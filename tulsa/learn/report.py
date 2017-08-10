from tulsa.learn.feature_groups import feature_groups
import pandas as pd
import numpy as np
from datetime import datetime
from os import path, mkdir
import logging


def write_dated_csv(df, name, test_name, output_dir, str_today):
    # df = df.dropna()
    fname = '{}__cohort_{}__predicted_on_{}.csv'.format(name, test_name, str_today)
    floc = path.join(output_dir, fname)
    df.to_csv(floc, float_format='%.3f', index=False)


def last_score(df):
    ndf = df.dropna()
    ndfs = ndf.sort_values(by=['measured_year', 'season_order'], ascending=False)
    try:
        return ndfs['y_preds'].iloc[0]
    except:
        return None


def make_stu_feat_df(label_feature_df, stuterm_df, feats):
    '''
    return a dataframe of students and lowest
    (most needing improvement) feature values
    given a list of feature importances.
    :param stuterm_df: a student-term dataframe
    :type stuterm_df: pandas DataFrame
    :param label_feature_df: a student-term dataframe
    :type label_feature_df: pandas DataFrame
    :parm feats: feature importance
    :type feats: pandas DataFrame
    :returns dict[int:str]: between student ID and their n loweest features
    '''
    feats['name_stem'] = feats['feat_name'].apply(lambda x: x.split('___')[0])
    feats_action = feats[feats['name_stem'].isin(feature_groups['actionable'])]
    # the most negative ones
    feats_action_sorted = feats_action.sort_values('feat_imp', ascending=True)
    # just the negative ones
    feats_action_sorted_top = feats_action_sorted[feats_action_sorted['feat_imp'] < 0]
    if len(feats_action_sorted_top) == 0:
        logging.info('There are no negative features. NOTHING GOOD CAN COME OF THIS')
        return None
    top_feats = list(feats_action_sorted_top['feat_name'])
    logging.info('top feats were %s', top_feats)
    df_top_feats = label_feature_df[top_feats]
    # find the column for which the students are most deficient
    # in highly effective habits of...
    most_room = df_top_feats.idxmin(axis=1)
    most_room.name = 'most_room'
    stuterm_room = pd.concat([stuterm_df['studentid'], most_room], axis=1)
    stu_room = stuterm_room.groupby(by='studentid').agg(max).reset_index()
    return stu_room

def make_max_mean_latest(df):
    students_max = df.groupby('studentid')['y_preds'].agg(max)
    students_mean = df.groupby('studentid')['y_preds'].agg(np.mean)
    students_last = df.groupby('studentid').apply(last_score)

    all_df = pd.concat([students_max, students_mean, students_last], axis=1)
    all_df.columns = ['max_risk', 'mean_risk', 'latest_risk']
    return all_df.reset_index()


def make_stu_school_df(engine):
    """
    :param engine: a conn to database
    :type engine: sqlalchemy connection

    :returns: latest student-school data in following format:
              (student_number, school_id, school_name, grade)
    :rtype: pandas DataFrame
    """
    school_stu_sql = """
                     SELECT
                         student_number,
                         school_id,
                         school_name,
                         grade_level
                     FROM
                         clean_data.demographics
                         INNER JOIN (SELECT
                                         student_number,
                                         MAX(start_year) AS start_year
                                     FROM
                                         clean_data.demographics
                                     GROUP BY
                                         student_number) AS most_recent
                             USING (student_number, start_year)
                     """
    stu_school_df = pd.read_sql(school_stu_sql, engine)
    return stu_school_df


def write_report(stu_school_df, stu_most_improv, y_preds, test_name):
    """
    Write the final report in CSV format for tulsa based on y_predictions
    :param stuterm_df: dataframe containing stutends and terms
    :param schoolid_df: dataframe containing student-schoolid relation
    :param y_preds: the label predictions for the student terms
    :type stuterm_df: pandas DataFrame
    :type schoolid_df: pandas DataFrame
    :type y_preds: pandas DataFrame
    """
    # some setup
    csv_dir = path.abspath('/mnt/data/tulsa/csv-output/')
    today = datetime.today()
    str_today = today.strftime('%d_%m_%Y')
    output_dir = path.join(csv_dir, str_today)

    if not path.exists(output_dir):
        mkdir(output_dir)
        logging.info('made dir %s', output_dir)
    else:
        logging.info('already exists dir %s', output_dir)

    y_preds['season_order'] = y_preds['season'].apply(lambda x:
                                                      {'fall': 1, 'winter': 2, 'spring': 3}[x])
    y_preds_pre = y_preds[['studentid', 'measured_year', 'season_order', 'y_preds']]
    y_preds_mnml = make_max_mean_latest(y_preds_pre)
    y_preds_combined = y_preds_mnml.merge(stu_school_df, how='left',
                                          left_on='studentid',
                                          right_on='student_number')
    col_list = ['student_number', 'school_id', 'school_name',
                'grade_level', 'max_risk', 'mean_risk', 'latest_risk']
    # check if most_improve could be made
    if stu_most_improv is not None:
        # they could be made.
        y_preds_combined = y_preds_combined.merge(stu_most_improv, how='left')
        col_list.append('most_room')

    y_preds_combined.sort_values(by='latest_risk', ascending=False, inplace=True)
    logging.debug('columns of output are %s', col_list)
    final = y_preds_combined[col_list]
    write_dated_csv(final, 'all_schools',
                    test_name, output_dir, str_today)

    for school_id, schooldf in final.groupby(by='school_id'):
        logging.debug('working on school_id %s', school_id)
        school_rep = schooldf
        write_dated_csv(school_rep, 'school_{}'.format(school_id),
                        test_name, output_dir, str_today)
