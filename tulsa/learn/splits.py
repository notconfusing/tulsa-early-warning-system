import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split


def make_splits(split_strategy, stuterm_df, label_feature_df, engine):
    """
    Makes a list of (X_test, X_train, y_test, y_train) splits 
    :param split_strategy: refers to type of split used
    :param stuterm_label_feature_df: studentid, year, season, label, feature data
    :param engine: a db engine to use
    :type split_strategy: str
    :type stuterm_label_feature_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: list of four pandas DataFrames -- X_ dfs have features, y_ dfs have labels
    """
    if split_strategy == '80/20':
        X = label_feature_df.iloc[:,1:].as_matrix()
        y = label_feature_df.iloc[:,0].as_matrix()
        return [train_test_split(X, y, test_size=0.2, random_state=0)]
    elif split_strategy == 'cohort':
        return make_cohort_test_train_split(stuterm_df,label_feature_df, engine)
    elif split_strategy == 'predict_new':
        return make_second_grade_train_predict_split(stuterm_df,label_feature_df, engine)
    else:
        # no such split strategy
        raise NotImplementedError


def make_cohort_test_train_split(stuterm_df, label_feature_df, engine):
    """
    Makes a list of (X_test, X_train, y_test, y_train) splits based on cohort splitting strategy
    :param stuterm_label_feature_df: studentid, year, season, label, feature data
    :param engine: a db engine to use
    :type stuterm_label_feature_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: list of four pandas DataFrames -- X_ dfs have features, y_ dfs have labels
    """
    stuterm_df['grade'] = make_grade_column(stuterm_df, engine)
    splits = {}
    grade2_years = ['13_14', '14_15']
    for test_year in grade2_years:
        train_years = [year for year in grade2_years if year != test_year]
        train_ids = stuterm_df.loc[(stuterm_df['measured_year'].isin(train_years))&(stuterm_df['grade']==2), 'studentid']
        test_ids = stuterm_df.loc[(stuterm_df['measured_year']==test_year)&(stuterm_df['grade']==2), 'studentid']
        train_stuterm = stuterm_df[stuterm_df['studentid'].isin(train_ids)]
        test_stuterm = stuterm_df[stuterm_df['studentid'].isin(test_ids)]
        train_indexes = train_stuterm.index
        test_indexes = test_stuterm.index
        X_train = label_feature_df.iloc[train_indexes, 1:]
        X_test = label_feature_df.iloc[test_indexes, 1:]
        y_train = label_feature_df.iloc[train_indexes, 0]
        y_test = label_feature_df.iloc[test_indexes, 0]
        splits[test_year] = {'X_train': X_train,
                             'X_test': X_test,
                             'y_train': y_train,
                             'y_test': y_test,
                             'train_stuterm': train_stuterm,
                             'test_stuterm': test_stuterm}
    return splits


def make_second_grade_train_predict_split(stuterm_df, label_feature_df, engine):
    """
    Makes a list of (X_test, X_train, y_test, y_train) splits based on splitting strategy
    where all training set is all students who have completed grade 3 
    and test set is those who have not completed to be predicted
    NOTE: returns y_test but this is superfluous 
    :param stuterm_label_feature_df: studentid, year, season, label, feature data
    :param engine: a db engine to use
    :type stuterm_label_feature_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: list of four pandas DataFrames -- X_ dfs have features, y_ dfs have labels
    """
    stuterm_df['grade'] = make_grade_column(stuterm_df, engine)
    grade2_years = ['13_14', '14_15']
    test_year = '15_16'
    train_years = [year for year in grade2_years if year != test_year]
    train_ids = stuterm_df.loc[(stuterm_df['measured_year'].isin(train_years))&(stuterm_df['grade']==2), 'studentid']
    test_ids = stuterm_df.loc[(stuterm_df['measured_year']==test_year)&(stuterm_df['grade']==2), 'studentid']
    train_stuterm = stuterm_df[stuterm_df['studentid'].isin(train_ids)]
    test_stuterm = stuterm_df[stuterm_df['studentid'].isin(test_ids)]
    train_indexes = train_stuterm.index
    test_indexes = test_stuterm.index
    X_train = label_feature_df.iloc[train_indexes, 1:]
    X_test = label_feature_df.iloc[test_indexes, 1:]
    y_train = label_feature_df.iloc[train_indexes, 0]
    y_test = label_feature_df.iloc[test_indexes, 0]
    splits = {}
    splits[test_year] = {'X_train': X_train,
                             'X_test': X_test,
                             'y_train': y_train,
                             'y_test': y_test,
                             'train_stuterm': train_stuterm,
                             'test_stuterm': test_stuterm}
    return splits

def make_grade_column(stuterm_df, engine):
    """
    Appends a column indicate which grade a student belongs to. 
    :param stuterm_label_feature_df: studentid, year, season, label, feature data
    :param engine: a db engine to use
    :type stuterm_label_feature_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame 
    """
    dem_query = """
                SELECT student_number, grade_level, measured_year 
                FROM clean_data.demographics
                """
    dem = pd.read_sql_query(dem_query, engine)
    #join stuterm_df with grades 
    df = stuterm_df.merge(dem, how = 'left', 
                          left_on = ['studentid', 'measured_year'], 
                          right_on = ['student_number', 'measured_year'])
    # Need to fill in NA grades
    # but only if NA year is less than grade 3 year
    sid_na = list(set(df.loc[np.isnan(df['grade_level']), 'studentid']))
    for sid in sid_na:
        gr3_year = df.loc[(df['studentid']==sid) & (df['grade_level']==3), 'measured_year'].tail(1)
        if len(gr3_year)==0:
            pass
        else:
            na_year = df.loc[(df['studentid']==sid) & (np.isnan(df['grade_level'])), 'measured_year'].head(1)
            if int(str.split(gr3_year.iloc[0,], "_")[0]) > int(str.split(na_year.iloc[0,], "_")[0]):
                imp_grade = 3 - (int(str.split(gr3_year.iloc[0,], "_")[0]) - int(str.split(na_year.iloc[0,], "_")[0]))
                df.loc[(df['studentid']==sid)&(np.isnan(df['student_number'])), 'grade_level'] = imp_grade
            else:
                pass
    return df['grade_level']
