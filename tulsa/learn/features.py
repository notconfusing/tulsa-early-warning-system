"""
Module to generate features.

The features module will take in the model feature list and generate those
features for the model evaluation step.
"""

import pandas as pd
import numpy as np
import datetime

from tulsa.learn import helpers


def stuterm_labels_map_generic(stuterm_df, engine, latest_grade, flipped=False):
    """
    Generates eventual not 186 MAP score label
    based on the latest_grade completed

    :param stuterm_df: None gets passed through
    :type None:
    :param engine: a db engine to use
    :type engine: sqlalchemy engine
    :param latest_grade: the latest grade a student must have completed
    :type latest_grade: int
    :param flipped: whether to flip the label to get NOT NOT eventual 186
    :type flipped: bool

    :returns: studentid, year, season data
    :rtype: pandas DataFrame
    :returns: eventual 186 label
    :rtype: pandas Series
    """
    equality = '<' if not flipped else '>='
    label_sql = """
                WITH latest_or_bust AS (
                    SELECT distinct student_number
                    FROM clean_data.demographics
                    WHERE grade_level >= {latest_grade}
                ),
                eventual186 AS (
                    SELECT
                        map.studentid,
                        CASE
                            WHEN MAX(testritscore) {equality} 186
                                THEN 1
                            ELSE
                                0
                        END AS eventual186
                    FROM
                        clean_data.map
                        INNER JOIN latest_or_bust
                            ON map.studentid = latest_or_bust.student_number
                    WHERE
                        discipline = 'Reading'
                    GROUP BY
                        studentid
                ),
                second_and_down AS (
                    SELECT
                        student_number
                    FROM
                        clean_data.demographics
                    WHERE
                        grade_level <= 2
                )

                SELECT
                    DISTINCT eventual186,
                    studentid,
                    measured_year,
                    season
                FROM
                    clean_data.map
                    INNER JOIN eventual186
                        USING (studentid)
                    INNER JOIN second_and_down
                        ON map.studentid = second_and_down.student_number
                WHERE
                    discipline = 'Reading'
                    AND eventual186 IS NOT NULL;
                """.format(latest_grade=latest_grade, equality=equality)
    df = pd.read_sql_query(label_sql, engine)
    stuterm_df = df[['studentid', 'measured_year', 'season']]
    labels = df['eventual186']
    return stuterm_df, labels


def stuterm_labels_map_generic_omit_passing(stuterm_df, engine, latest_grade, flipped=False):
    '''
    Generates eventual not 186 MAP score label
    based on the latest_grade completed

    :param stuterm_df: None gets passed through
    :type None:
    :param engine: a db engine to use
    :type engine: sqlalchemy engine
    :param latest_grade: the latest grade a student must have completed
    :type latest_grade: int
    :param flipped: whether to flip the label to get NOT NOT eventual 186
    :type flipped: bool

    :returns: studentid, year, season data
    :rtype: pandas DataFrame
    :returns: eventual 186 label
    :rtype: pandas Series
    '''
    passing_label = 1 if not flipped else 0
    failing_label = 1 - passing_label
    label_sql = """
                WITH latest_or_bust AS (
                    SELECT distinct student_number
                    FROM clean_data.demographics
                    WHERE grade_level >= {latest_grade}
                ),
                first_pass_score AS (
                SELECT
                    studentid,
                    MIN(TO_DATE(teststartdate, 'MM/DD/YYYY')) AS first_pass_date
                FROM
                    clean_data.map
                WHERE
                    testritscore >= 186
                    AND discipline = 'Reading'
                GROUP BY
                    studentid
                ),
                eventual186 AS (
                    SELECT
                        map.studentid,
                        map.teststartdate,
                        CASE
                            WHEN first_pass_date IS NULL
                                THEN {passing}
                            WHEN first_pass_date >= TO_DATE(map.teststartdate, 'MM/DD/YYYY')
                                THEN {failing}
                            ELSE
                                NULL
                        END AS eventual186
                    FROM
                        clean_data.map
                        INNER JOIN latest_or_bust
                            ON map.studentid = latest_or_bust.student_number
                        LEFT JOIN first_pass_score
                            ON (first_pass_score.studentid = map.studentid)
                    WHERE
                        discipline = 'Reading'
                ),
                second_and_down AS (
                    SELECT
                        student_number
                    FROM
                        clean_data.demographics
                    WHERE
                        grade_level <= 2
                )

                SELECT
                    DISTINCT eventual186,
                    studentid,
                    measured_year,
                    season
                FROM
                    clean_data.map
                    INNER JOIN eventual186
                        USING (studentid, teststartdate)
                    INNER JOIN second_and_down
                        ON map.studentid = second_and_down.student_number
                WHERE
                    discipline = 'Reading'
                    AND eventual186 IS NOT NULL;
                """.format(latest_grade=latest_grade, passing=passing_label, failing=failing_label)
    df = pd.read_sql_query(label_sql, engine)
    stuterm_df = df[['studentid', 'measured_year', 'season']]
    labels = df['eventual186']
    return stuterm_df, labels


def stuterm_labels_eventual_not_186(latest_grade, flipped=False):
    """
    Higher order function make a stuterm generating function based on
    latest grade, and support label flipping.
    :param latest_grade: the latest grade a student must have completed
    :type latest_grade: int
    :param flipped: whether to flip the label to get NOT NOT eventual 186
    :type flipped: bool
    """
    return lambda stuterm_df, engine: \
        stuterm_labels_map_generic(stuterm_df, engine, latest_grade, flipped=flipped)


def stuterm_labels_eventual_not_186_omit_passing(latest_grade, flipped=False):
    """
    Higher order function make a stuterm generating function based on
    latest grade, and support label flipping.
    Omits stuterms that are after a student achieves passing.
    
    :param latest_grade: the latest grade a student must have completed
    :type latest_grade: int
    :param flipped: whether to flip the label to get NOT NOT eventual 186
    :type flipped: bool
    """
    return lambda stuterm_df, engine: \
        stuterm_labels_map_generic_omit_passing(stuterm_df, engine, latest_grade, flipped=False)


def stuterm_labels_eventual_186_omit_passing(latest_grade, flipped=True):
    '''
    Higher order function make a stuterm generating function based on
    latest grade, and support label flipping.
    :param latest_grade: the latest grade a student must have completed
    :type latest_grade: int
    :param flipped: whether to flip the label to get NOT NOT eventual 186
    :type flipped: bool
    '''
    return lambda stuterm_df, engine: \
        stuterm_labels_map_generic_omit_passing(stuterm_df, engine, latest_grade, flipped=True)


def get_dem_sql(dem_col, static=False):
    """
    SQL shell for demographics data. If feature is static, then
    most recent record is applied for that student.

    :param dem_col: specific demographics table column name
    :type dem_col: str
    :param static: whether demographics feature is static
    :type static: bool

    :returns: full sql statement
    :rtype: str
    """
    dem_sql = """
              SELECT
                dem.measured_year,
                dem.student_number
                , {dem_column}
              FROM
                  clean_data.demographics AS dem
              """.format(dem_column=dem_col)
    if static:
        dem_sql = dem_sql + """INNER JOIN
                                   (SELECT
                                       student_number,
                                       MAX(start_year) AS start_year
                                   FROM
                                       clean_data.demographics
                                   GROUP BY
                                          student_number) AS most_recent_record
                               USING (student_number, start_year)"""
    return dem_sql


def female_feature(stuterm_df, engine):
    """
    Generates whether student is female feature, based on last demographics
    file student is represented in

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: is female feature
    :rtype: pandas DataFrame
    """
    gender_col = """CASE gender
                        WHEN 'F' THEN 1
                        WHEN 'M' THEN 0
                        ELSE -1
                    END AS is_female
                 """
    gender_sql = get_dem_sql(gender_col, static=True)
    is_female_df = pd.read_sql_query(gender_sql, engine)
    stuterm_female_df = stuterm_df.merge(is_female_df[['student_number',
                                                       'is_female']],
                                         how='left',
                                         left_on='studentid',
                                         right_on='student_number')
    return stuterm_female_df['is_female']


def ethnicity_feature(stuterm_df, engine):
    """
    Generates student ethnicity binary matrix, based on last demographics
    file student is represented in

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: ethnicity feature 
    :rtype: pandas DataFrame
    """
    ethnicity_col = "ethnicity"
    ethnicity_sql = get_dem_sql(ethnicity_col, static=True)
    ethnicity_df = pd.read_sql_query(ethnicity_sql, engine)
    stuterm_eth_df = stuterm_df.merge(ethnicity_df[['student_number',
                                                    'ethnicity']],
                                      how='left',
                                      left_on='studentid',
                                      right_on='student_number')
    return stuterm_eth_df['ethnicity']


def age_feature(stuterm_df, engine):
    """
    Generates student age (in months) feature based on month diff of birth
    date and term start date

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns:
    :rtype:
    """
    age_sql = """
              WITH student_dob AS (
                SELECT
                    DISTINCT student_number,
                    dob
                FROM
                    clean_data.demographics
              )

              SELECT
                  DISTINCT map.measured_year,
                  student_dob.student_number,
                  map.season,
                  CASE map.season
                      WHEN 'fall'
                          THEN (TO_DATE('20' || map.cal_year || '-08-01',
                              'YYYY-MM-DD') - dob)/30
                      WHEN 'winter'
                          THEN (TO_DATE('20' || map.cal_year || '-01-01',
                              'YYYY-MM-DD') - dob)/30
                      WHEN 'spring'
                          THEN (TO_DATE('20' || map.cal_year || '-03-01',
                              'YYYY-MM-DD') - dob)/30
                  END AS age_in_months
              FROM
                  student_dob
                  INNER JOIN clean_data.map AS map
                      ON (student_dob.student_number = map.studentid)
              WHERE
                  map.discipline = 'Reading'
                  AND student_dob.dob >= TO_DATE('1970-01-01', 'YYYY-MM-DD');
              """
    age_df = pd.read_sql_query(age_sql, engine)
    stuterm_age_df = stuterm_df.merge(age_df[['measured_year',
                                              'student_number',
                                              'season',
                                              'age_in_months']],
                                      how='left',
                                      left_on=['studentid',
                                               'measured_year',
                                               'season'],
                                      right_on=['student_number',
                                                'measured_year',
                                                'season'])
    return stuterm_age_df['age_in_months']


def ell_feature(stuterm_df, engine):
    """
    Generates whether students are in ELL feature for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: in ell feature
    :rtype: pandas DataFrame
    """
    ell_col = "CASE WHEN ok_ell IS NULL THEN '0' ELSE ok_ell END AS in_ell"
    ell_sql = get_dem_sql(ell_col)
    in_ell_df = pd.read_sql_query(ell_sql, engine)
    stuterm_ell_df = stuterm_df.merge(in_ell_df, how='left',
                                      left_on=['studentid',
                                               'measured_year'],
                                      right_on=['student_number',
                                                'measured_year'])
    return stuterm_ell_df['in_ell']


def ell_lang_feature(stuterm_df, engine):
    """
    Generates student ELL language feature (if any) for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: ell language code feature
    :rtype: pandas DataFrame
    """
    ell_lang_col = """CASE WHEN ok_ell_language_code IS NULL
                          THEN '0'
                      ELSE ok_ell_language_code
                      END AS language_code"""
    ell_lang_sql = get_dem_sql(ell_lang_col)
    ell_lang_df = pd.read_sql_query(ell_lang_sql, engine)
    stuterm_lang_df = stuterm_df.merge(ell_lang_df, how='left',
                                       left_on=['studentid',
                                                'measured_year'],
                                       right_on=['student_number',
                                                 'measured_year'])
    return stuterm_lang_df['language_code']


def disability_code_feature(stuterm_df, engine):
    """
    Generates student disability type feature for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: disability code feature
    :rtype: pandas DataFrame
    """
    disability_col = """CASE WHEN ok_primary_disability_code IS NULL
                            THEN '0'
                        ELSE ok_primary_disability_code
                        END AS disability_code"""
    disability_sql = get_dem_sql(disability_col)
    disability_df = pd.read_sql_query(disability_sql, engine)
    stuterm_disability_df = stuterm_df.merge(disability_df, how='left',
                                             left_on=['studentid',
                                                      'measured_year'],
                                             right_on=['student_number',
                                                       'measured_year'])
    return stuterm_disability_df['disability_code']


def service_delivery_feature(stuterm_df, engine):
    """
    Generates student service delivery feature for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: service delivery code feature
    :rtype: pandas DataFrame
    """
    service_delivery_col = """CASE WHEN tps_service_delivery_code IS NULL
                                  THEN '0'
                              ELSE tps_service_delivery_code
                              END AS service_delivery_code"""
    service_delivery_sql = get_dem_sql(service_delivery_col)
    service_delivery_df = pd.read_sql_query(service_delivery_sql, engine)
    stuterm_service_delivery_df = stuterm_df.merge(service_delivery_df,
                                                   how='left',
                                                   left_on=['studentid',
                                                            'measured_year'],
                                                   right_on=['student_number',
                                                             'measured_year'])
    return stuterm_service_delivery_df['service_delivery_code']


def lunch_feature(stuterm_df, engine):
    """
    Generates student lunch type for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: lunch status feature
    :rtype: pandas DataFrame
    """
    lunch_col = """CASE WHEN lunch_status IS NULL
                       THEN '0'
                       ELSE lunch_status
                   END AS lunch"""
    lunch_sql = get_dem_sql(lunch_col)
    lunch_df = pd.read_sql_query(lunch_sql, engine)
    stuterm_lunch_df = stuterm_df.merge(lunch_df, how='left',
                                        left_on=['studentid',
                                                 'measured_year'],
                                        right_on=['student_number',
                                                  'measured_year'])
    return stuterm_lunch_df['lunch']


def homeless_feature(stuterm_df, engine):
    """
    Generates student homelessness for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: is homeless feature
    :rtype: pandas DataFrame
    """
    homeless_col = """CASE WHEN ok_homeless IS NULL
                          THEN '0'
                          ELSE ok_homeless
                      END AS homeless"""
    homeless_sql = get_dem_sql(homeless_col)
    homeless_df = pd.read_sql_query(homeless_sql, engine)
    stuterm_homeless_df = stuterm_df.merge(homeless_df, how='left',
                                           left_on=['studentid',
                                                    'measured_year'],
                                           right_on=['student_number',
                                                     'measured_year'])
    return stuterm_homeless_df['homeless']


def lives_with_feature(stuterm_df, engine):
    """
    Generates student guardianship for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: lives with [parent] type feature
    :rtype: pandas DataFrame
    """
    lives_with_col = """CASE WHEN tps_demographics_lives_with IS NULL
                            THEN '0'
                            ELSE tps_demographics_lives_with
                        END AS lives_with"""
    lives_with_sql = get_dem_sql(lives_with_col)
    lives_with_df = pd.read_sql_query(lives_with_sql, engine)
    stuterm_lives_with_df = stuterm_df.merge(lives_with_df, how='left',
                                             left_on=['studentid',
                                                      'measured_year'],
                                             right_on=['student_number',
                                                       'measured_year'])
    return stuterm_lives_with_df['lives_with']


def school_feature(stuterm_df, engine):
    """
    Generates what schools students are enrolled in for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: school feature
    :rtype: pandas DataFrame
    """
    school_col = """CASE WHEN school_id IS NULL
                       THEN '0'
                       ELSE school_id
                   END AS school_id"""
    school_sql = get_dem_sql(school_col)
    school_df = pd.read_sql_query(school_sql, engine)
    stuterm_school_df = stuterm_df.merge(school_df, how='left',
                                         left_on=['studentid',
                                                  'measured_year'],
                                         right_on=['student_number',
                                                   'measured_year'])
    return stuterm_school_df['school_id']


def map_season(stuterm_df, engine):
    """which academic season a test was taken in
    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :returns: pandas DataFrame -- map season feature
    """
    return stuterm_df['season']


def hour_of_day(timestr):
    """hour of time of day -- 24H

    :param timestr: time string in format '%H:%M:%S'
    :type timestr: str
    :returns: int representing hour
    """
    time = datetime.datetime.strptime(timestr, '%H:%M:%S')
    return time.hour


def days_since_first_map(datestr):
    """number of days since the the first MAP test in tulsa was issued
    uses hardcoded first day as 2013/09/09

    :param timestr: time string in format '%H:%M:%S'
    :type timestr: str
    :returns: int representing day count
    """
    first_map = datetime.datetime(2013, 9, 9).toordinal()
    this_map = datetime.datetime.strptime(datestr, '%m/%d/%Y').toordinal()
    return this_map - first_map


def map_feat_generic(stuterm_df, engine, map_col, where_statement, agg_fun):
    """Generic function to make map features

    :param map_col: the column to use in the clean_dat.map table
    :param stuterm_df: studentid, year, season data
    :param agg_fun: the aggregration function to pass to groupby
    :param engine: a db engine to use
    :type map_col: str
    :type stuterm_df: pandas DataFrame
    :type agg_fun: function
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame or Series with numeric features
    """
    map_select_sql = """select {map_col}, studentid, measured_year, season
    from clean_data.map {where_statement}""".format(map_col=map_col, where_statement=where_statement)

    map_col_df = pd.read_sql_query(map_select_sql, engine)
    maxperterm_df = map_col_df.groupby(by=['studentid', 'measured_year',
                                           'season']).agg(agg_fun) \
                                                     .reset_index()
    merged_df = stuterm_df.merge(maxperterm_df,
                                 how='left',
                                 left_on=['studentid',
                                          'measured_year',
                                          'season'],
                                 right_on=['studentid',
                                           'measured_year',
                                           'season'])

    return merged_df[map_col]


def make_map_feature(feature_str):
    """Make features that utilize the map dataset

    :param feature_str: the name of the feature to make
    :type feature_str: str
    :returns: function that will accept stuterm_df and engine
    """
    map_args = {'map_testritscore': {'map_col': 'testritscore',
                                     'where_statement': "",
                                     'agg_fun': np.max},
                'map_testpercentile': {'map_col': 'testpercentile',
                                       'where_statement': "",
                                       'agg_fun': np.max},
                'map_testdurationminutes': {'map_col': 'testdurationminutes',
                                            'where_statement': "",
                                            'agg_fun': np.max},
                'map_percentcorrect': {'map_col': 'percentcorrect',
                                       'where_statement': "",
                                       'agg_fun': np.max},
                'map_start_date': {'map_col': 'teststartdate',
                                   'where_statement': "",
                                   'agg_fun': lambda x: np.max(x.apply(days_since_first_map))},
                'map_start_hour': {'map_col': 'teststarttime',
                                   'where_statement': "",
                                   'agg_fun': lambda x: np.max(x.apply(hour_of_day))},
                'map_reading_testritscore': {'map_col': 'testritscore',
                                             'where_statement': "where discipline = 'Reading'",
                                             'agg_fun': np.max},
                'map_reading_testpercentile': {'map_col': 'testpercentile',
                                               'where_statement': "where discipline = 'Reading'",
                                               'agg_fun': np.max},
                'map_reading_testdurationminutes': {'map_col': 'testdurationminutes',
                                                    'where_statement': "where discipline = 'Reading'",
                                                    'agg_fun': np.max},
                'map_reading_percentcorrect': {'map_col': 'percentcorrect',
                                               'where_statement': "where discipline = 'Reading'",
                                               'agg_fun': np.max},
                'map_reading_start_date': {'map_col': 'teststartdate',
                                           'where_statement': "where discipline = 'Reading'",
                                           'agg_fun': lambda x: np.max(x.apply(days_since_first_map))},
                'map_reading_start_hour': {'map_col': 'teststarttime',
                                           'where_statement': "where discipline = 'Reading'",
                                           'agg_fun': lambda x: np.max(x.apply(hour_of_day))}
                }

    map_col = map_args[feature_str]['map_col']
    where_statement = map_args[feature_str]['where_statement']
    agg_fun = map_args[feature_str]['agg_fun']

    return lambda stuterm_df, engine: map_feat_generic(stuterm_df, engine,
                                                       map_col, where_statement, agg_fun)


def find_ac_year(year, season):
    """returns the string representation of academic year, given a year and season
    Example: find_join_year('2014', 'fall') -> 14_15
    Example: find_join_year('2014', 'winter') -> 13_14

    :param year: the 4 digit year in question
    :param season: one of 'fall', 'spring', 'winter'
    :type year: str
    :type season: str
    :returns str:
    """
    if season == 'fall':
        start, end = year[-2:], str(int(year) + 1)[-2:]
    elif season in ['winter', 'spring']:
        start, end = str(int(year) - 1)[-2:], year[-2:]
    return '{}_{}'.format(start, end)


def tripod_feat_generic(stuterm_df, engine, tripod_col, agg_fun):
    """Generic function to make map features
    :param tripod_col: the column to use in the clean_data.tripod table
    :param stuterm_df: studentid, year, season data
    :param agg_fun: the aggregration function to pass to groupby
    :param engine: a db engine to use
    :type tripod_col: str
    :type stuterm_df: pandas DataFrame
    :type agg_fun: function
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame or Series with numeric features
    """
    tripod_select_sql = """select * from
                    (SELECT {tripod_col}, yr, season as tripod_season, teacher_id 
                    FROM clean_data.tripod) as t

                    inner join

                    (SELECT student_number, measured_year, season, teachernumber
                    FROM clean_data.roster) as r

                    on t.teacher_id = r.teachernumber 
                       and t.yr = cast(r.measured_year as int)
                       and lower(t.tripod_season) = lower(r.season)""".format(tripod_col=tripod_col)

    tripod_col_df = pd.read_sql_query(tripod_select_sql, engine)
    tripod_col_df['ac_measured_year'] = tripod_col_df[['measured_year', 'season']].apply(
        lambda x: find_ac_year(x['measured_year'], x['season']), axis=1)
    aggperterm_df = tripod_col_df.groupby(by=['student_number', 'ac_measured_year', 'season']).agg(agg_fun).reset_index()
    merged_df = stuterm_df.merge(aggperterm_df,
                                 how='left',
                                 left_on=['studentid', 'measured_year', 'season'],
                                 right_on=['student_number', 'ac_measured_year', 'season'])

    return merged_df[tripod_col]


def make_tripod_feature(feature_str):
    """Make features that utilize the map dataset
    :param feature_str: the name of the feature to make
    :type feature_str: str
    :returns: function that will accept stuterm_df and engine
    """
    tripod_args = {'tripod_challenge_min': {'tripod_col': 'challenge',
                                            'agg_fun': np.min},
                   'tripod_challenge_max': {'tripod_col': 'challenge',
                                            'agg_fun': np.max},
                   'tripod_challenge_mean': {'tripod_col': 'challenge',
                                             'agg_fun': np.mean},
                   'tripod_challenge_std': {'tripod_col': 'challenge',
                                            'agg_fun': np.std},
                   'tripod_classroom_management_min': {'tripod_col': 'classroom_management',
                                                       'agg_fun': np.min},
                   'tripod_classroom_management_max': {'tripod_col': 'classroom_management',
                                                       'agg_fun': np.max},
                   'tripod_classroom_management_mean': {'tripod_col': 'classroom_management',
                                                        'agg_fun': np.mean},
                   'tripod_classroom_management_std': {'tripod_col': 'classroom_management',
                                                       'agg_fun': np.std},
                   'tripod_captivate_min': {'tripod_col': 'captivate',
                                            'agg_fun': np.min},
                   'tripod_captivate_max': {'tripod_col': 'captivate',
                                            'agg_fun': np.max},
                   'tripod_captivate_mean': {'tripod_col': 'captivate',
                                             'agg_fun': np.mean},
                   'tripod_captivate_std': {'tripod_col': 'captivate',
                                            'agg_fun': np.std},
                   'tripod_care_min': {'tripod_col': 'care',
                                       'agg_fun': np.min},
                   'tripod_care_max': {'tripod_col': 'care',
                                       'agg_fun': np.max},
                   'tripod_care_mean': {'tripod_col': 'care',
                                        'agg_fun': np.mean},
                   'tripod_care_std': {'tripod_col': 'care',
                                       'agg_fun': np.std},
                   'tripod_clarify_min': {'tripod_col': 'clarify',
                                          'agg_fun': np.min},
                   'tripod_clarify_max': {'tripod_col': 'clarify',
                                          'agg_fun': np.max},
                   'tripod_clarify_mean': {'tripod_col': 'clarify',
                                           'agg_fun': np.mean},
                   'tripod_clarify_std': {'tripod_col': 'clarify',
                                          'agg_fun': np.std},
                   'tripod_consolidate_min': {'tripod_col': 'consolidate',
                                              'agg_fun': np.min},
                   'tripod_consolidate_max': {'tripod_col': 'consolidate',
                                              'agg_fun': np.max},
                   'tripod_consolidate_mean': {'tripod_col': 'consolidate',
                                               'agg_fun': np.mean},
                   'tripod_consolidate_std': {'tripod_col': 'consolidate',
                                              'agg_fun': np.std},
                   'tripod_confer_min': {'tripod_col': 'confer',
                                         'agg_fun': np.min},
                   'tripod_confer_max': {'tripod_col': 'confer',
                                         'agg_fun': np.max},
                   'tripod_confer_mean': {'tripod_col': 'confer',
                                          'agg_fun': np.mean},
                   'tripod_confer_std': {'tripod_col': 'confer',
                                         'agg_fun': np.std},
                   'tripod_cs_min': {'tripod_col': 'cs',
                                     'agg_fun': np.min},
                   'tripod_cs_max': {'tripod_col': 'cs',
                                     'agg_fun': np.max},
                   'tripod_cs_mean': {'tripod_col': 'cs',
                                      'agg_fun': np.mean},
                   'tripod_cs_std': {'tripod_col': 'cs',
                                     'agg_fun': np.std}}

    tripod_col = tripod_args[feature_str]['tripod_col']
    agg_fun = tripod_args[feature_str]['agg_fun']

    return lambda stuterm_df, engine: tripod_feat_generic(stuterm_df, engine, tripod_col, agg_fun)


def iread_enrolled(stuterm_df, engine):
    """
    Whether or not student is enrolled in iRead program (s44jr program)
    :param stuterm_df: studentid, year, season data
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame -- binary variable representing enrolled Y/N
    """
    query = """
                 SELECT
                 DISTINCT ON (sis_id, measured_year)
                    sis_id, measured_year, grade
                    , CASE s44jr_enrolled
                            WHEN 'Yes' THEN 1
                            WHEN 'No' THEN 0
                            ELSE -1
                       END AS iread_is_enrolled
                 FROM
                    clean_data.iread
                 GROUP BY sis_id, measured_year, grade, iread_is_enrolled   
                 ORDER BY sis_id, measured_year, iread_is_enrolled DESC;
            """
    is_enrolled_df = pd.read_sql_query(query, engine)
    stuterm_enrolled_df = stuterm_df.merge(is_enrolled_df, how='left',
                                           left_on=['studentid', 'measured_year'],
                                           right_on=['sis_id', 'measured_year'])
    return stuterm_enrolled_df['iread_is_enrolled']


def iread_data_missing(stuterm_df, engine):
    """
    Whether or not data on iRead is missing (s44jr program)
    :param stuterm_df: studentid, year, season data
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame -- binary variable representing data missing Y/N
    """
    query = """
                 SELECT
                 DISTINCT ON (sis_id, measured_year)
                    sis_id, measured_year, grade
                    , CASE s44jr_enrolled
                            WHEN 'Yes' THEN 1
                            WHEN 'No' THEN 0
                            ELSE -1
                       END AS iread_is_enrolled
                 FROM
                    clean_data.iread
                 GROUP BY sis_id, measured_year, grade, iread_is_enrolled   
                 ORDER BY sis_id, measured_year, iread_is_enrolled DESC;
            """
    is_enrolled_df = pd.read_sql_query(query, engine)
    stuterm_enrolled_df = stuterm_df.merge(is_enrolled_df, how='left',
                                           left_on=['studentid', 'measured_year'],
                                           right_on=['sis_id', 'measured_year'])
    df_dem = pd.read_sql_query('SELECT student_number, grade_level, measured_year from clean_data.demographics', engine)
    stuterm_dem_df = stuterm_enrolled_df.merge(df_dem, how='left',
                                               left_on=['studentid', 'measured_year'],
                                               right_on=['student_number', 'measured_year'])
    stuterm_dem_df['iread_data_missing'] = np.nan
    # only students below grade 3 take iRead
    stuterm_dem_df.loc[(np.isnan(stuterm_dem_df['iread_is_enrolled'])) & (stuterm_dem_df['grade_level']!=3), 'iread_data_missing'] = 1
    stuterm_dem_df.loc[(np.isfinite(stuterm_dem_df['iread_is_enrolled'])) & (stuterm_dem_df['grade_level']!=3), 'iread_data_missing'] = 0
    return stuterm_dem_df['iread_data_missing']


def iread_query_statement(column_names):
    """
    Creates a generic sql statement used in most of the iread feature generating functions
    :param column_names: specifies one or more column names to pull
    :type column_names: str or list
    :returns: string to be used as sql statement
    """
    if isinstance(column_names, list):
        col_names = ','.join(column_names)
    else:
        col_names = column_names
    query = """
                SELECT
                 DISTINCT ON (sis_id, measured_year)
                    sis_id, measured_year, grade, s44jr_enrolled, {col_names} 
                 FROM
                    clean_data.iread
                 GROUP BY sis_id, measured_year, grade, s44jr_enrolled, {col_names}
                 ORDER BY sis_id, measured_year, s44jr_enrolled DESC;
                 """.format(col_names = col_names)
    return query


def iread_took_screener(stuterm_df, engine):
    """
    Whether or not student took iRead program screener
    :param stuterm_df: studentid, year, season data
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame -- binary variable representing took screener Y/N
    """
    query = iread_query_statement('iread_screener_date_administered')
    took_screener_df = pd.read_sql_query(query, engine)
    took_screener_df['took_screener'] = np.nan
    took_screener_df.loc[(took_screener_df['s44jr_enrolled'] == "Yes") & (took_screener_df['iread_screener_date_administered'].isnull()), 'took_screener' ] = 0
    took_screener_df.loc[(took_screener_df['s44jr_enrolled'] == "Yes") & (took_screener_df['iread_screener_date_administered'].notnull()), 'took_screener' ] = 1
    stuterm_took_screener_df = stuterm_df.merge(took_screener_df, how='left',
                                                left_on=['studentid', 'measured_year'],
                                                right_on=['sis_id', 'measured_year'])
    
    return stuterm_took_screener_df['took_screener']


def iread_feature_generic(stuterm_df, iread_col, engine):
    """
    Generic function to make iread features
    :param stuterm_df: studentid, year, season data
    :param iread_col: string representing which iread column to extract
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :type iread_col: str
    :returns: pandas DataFrame or Series with numeric features
    """
    query = iread_query_statement(iread_col)
    feature_df = pd.read_sql_query(query, engine)
    stuterm_feature_df = stuterm_df.merge(feature_df, how='left',
                                          left_on=['studentid', 'measured_year'],
                                          right_on=['sis_id', 'measured_year'])
    return stuterm_feature_df[iread_col]


def iread_average_time_per_topic(stuterm_df, engine):
    """
    Returns average time (in minutes) student spent on each topic
    :param stuterm_df: studentid, year, season data
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame numeric representing minutes
    """
    query = iread_query_statement(['iread_daterange_total_topics_completed', 'iread_daterange_total_time'])
    feature_df = pd.read_sql_query(query, engine)
    feature_df['iread_average_time_per_topic'] = feature_df['iread_daterange_total_time']/ feature_df['iread_daterange_total_topics_completed']
    stuterm_feature_df = stuterm_df.merge(feature_df, how='left',
                                          left_on=['studentid', 'measured_year'],
                                          right_on=['sis_id', 'measured_year'])
    return stuterm_feature_df['iread_average_time_per_topic']


def iread_average_sessions_per_week(stuterm_df, engine):
    """
    Returns average number of sessions per week spent on iRead
    :param stuterm_df: studentid, year, season data
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame numeric representing average sessions
    """
    query = iread_query_statement(['iread_daterange_total_sessions', 'export_start_date', 'export_end_date'])
    feature_df = pd.read_sql_query(query, engine)
    feature_df['end_date'] = feature_df['export_end_date'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').toordinal())
    feature_df['start_date'] = feature_df['export_start_date'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').toordinal())
    feature_df['weeks'] = (feature_df['end_date'] - feature_df['start_date'])/7
    feature_df['iread_average_sessions_per_week'] = feature_df['iread_daterange_total_sessions']/ feature_df['weeks'] 
    stuterm_feature_df = stuterm_df.merge(feature_df, how='left',
                                          left_on=['studentid', 'measured_year'],
                                          right_on=['sis_id', 'measured_year'])
    return stuterm_feature_df['iread_average_sessions_per_week']


def convert_current_series_topic(x, level_type):
    """
    Returns an integer representing the current series or topic being completed by a student
    (helper function)
    :param x: a string from the raw 'iread_daterange_current_series_topic' column
    :param level_type: either 'series' or 'topic'
    :type x: str, depending on year is either in format 'series_x_topic_x' or 'xx.xx'
    :type level_type: str
    :returns: int representing current series or topic
    """
    if x == None:
        current_series = None
        current_topic = None
    elif 'series' in x:
        current_series = int(x.split('_')[1])
        current_topic = int(x.split('_')[3])
    else:
        current_series = int(x.split('.')[0])
        current_topic = int(x.split('.')[1])
    if level_type == 'series':
        return current_series
    else:
        return current_topic


def iread_current_series_topic(stuterm_df, engine, level_type):
    """
    Returns current series or topic
    :param stuterm_df: studentid, year, season data
    :param engine: a db engine to use
    :param level_type: either 'series' or 'topic'
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :type level_type: str
    :returns: pandas DataFrame int representing series or topic
    """
    query = iread_query_statement('iread_daterange_current_series_topic')
    feature_df = pd.read_sql_query(query, engine)
    feature_df['current_' + level_type] = feature_df['iread_daterange_current_series_topic'].apply(lambda x: convert_current_series_topic(x, level_type)) 
    stuterm_feature_df = stuterm_df.merge(feature_df, how='left',
                                          left_on=['studentid', 'measured_year'],
                                          right_on=['sis_id', 'measured_year'])
    return stuterm_feature_df['current_' + level_type]

def make_iread_current_series_topic(level_type):
    """
    Returns a function to generate current series or topic
    :param level_type: specifying 'series' or 'topic'
    :type level_type: str
    :returns: function that will accept stuterm_df and engine
    """
    return lambda stuterm_df, engine: iread_current_series_topic(stuterm_df, engine, level_type)

def make_iread_feature(feature_str):
    """Make features that utilize the iread dataset
    :param feature_str: the name of the feature to make
    :type feature_str: str
    :returns: function that will accept stuterm_df and engine
    """
    iread_args = {'iread_screener_placement_series': 'iread_screener_placement_series',
                  'iread_highest_unit_reached': 'iread_daterange_highest_unit_reached',
                  'iread_total_sessions': 'iread_daterange_total_sessions',
                  'iread_total_topics_completed': 'iread_daterange_total_topics_completed',
                  'iread_total_time': 'iread_daterange_total_time'}

    iread_col = iread_args[feature_str]

    return lambda stuterm_df, engine: iread_feature_generic(stuterm_df, iread_col, engine)


def course_taken_generic(stuterm_df, engine, course_or_grade, cg_value):                                                    
    """Generic function to make grades features
    :param stuterm_df: studentid, year, season data
    :param course_or_grade: one of ['course', 'grade']
    :param cg_value: the course category to subset one of
                                ['art', 'pe', 'read', 'science', 'math',
                                'social', 'computer', 'non-grade', 'language']
                     the grade category should be one of
                                ['a', 'b', 'c', 'd', 'e', 'f',
                                's', 'n', 'u', 'p', 'ng']
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type course: str
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame or Series with numeric features
    """
    grades_sql = """SELECT student_number, grade, course_name, termid
                    FROM clean_data.grades_16_uofc_grades_1st___3rd_2013_to_2
                    where grade_level <4"""
    grades_df = pd.read_sql(grades_sql, engine)
    grades_df['measured_year'] = grades_df['termid'] \
        .apply(helpers.termid_to_ac_year)
    if course_or_grade == 'course':
        select_col = 'course_name'
        cat_fun = helpers.categorize_courses
    elif course_or_grade == 'grade':
        select_col = 'grade'
        cat_fun = helpers.categorize_grades
    else:
        raise ValueError('course_or_grade must be "course" or "grade"')
    grades_df['cat'] = grades_df[select_col] \
        .apply(cat_fun)
    course_cat_only = grades_df[grades_df['cat'] == cg_value]
    course_minimal = course_cat_only[['student_number', 'measured_year',
                                      'cat']]
    course_per_stuterm = course_minimal.groupby(by=['student_number',
                                                    'measured_year']) \
        .agg(len).reset_index()
    merged_df = stuterm_df.merge(course_per_stuterm,
                                 how='left',
                                 left_on=['studentid', 'measured_year'],
                                 right_on=['student_number', 'measured_year'])
    return merged_df['cat']


def make_course_feature(course_or_grade, cg_value):
    """Make features that utilize the grades dataset
    :param feature_str: the name of the feature to make
    :type feature_str: str
    :returns: function that will accept stuterm_df and engine
    """
    return lambda stuterm_df, engine: course_taken_generic(stuterm_df, engine,
                                                           course_or_grade,
                                                           cg_value)


def rsa_logs_generic(stuterm_df, engine, subtype):
    """Generic function to make grades features
    :param stuterm_df: studentid, year, season data
    :param subtype: the type of RSA event must be one of
                    ["RSA_RETAINED","PASSED_ITBS","PROBATION_PROMOTED",
                     "PASSED_OCCT","EXEMPTION","MEETS_RSA_CRITERIA"]
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type course: str
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame or Series with numeric features
    """
    rsa_sql = """SELECT student_number, subtype, entry_date, discipline_incidentdate
                 FROM clean_data.rsa_logs
                 WHERE subtype like '{subtype}';""".format(subtype=subtype)
    rsa_df = pd.read_sql(rsa_sql, engine)
    rsa_df['measured_year'] = rsa_df['discipline_incidentdate'].apply(helpers.ac_year_from_date)
    rsa_df['season'] = rsa_df['discipline_incidentdate'].apply(helpers.season_from_date)
    count_per_term = rsa_df.groupby(by=['student_number', 'measured_year',
                                        'season']).agg(len).reset_index()
    merged_df = stuterm_df.merge(count_per_term,
                                 how='left',
                                 left_on=['studentid', 'measured_year', 'season'],
                                 right_on=['student_number', 'measured_year', 'season'])
    return merged_df['subtype']


def make_rsa_log_feature(subtype):
    """Make features that utilize the rsa_log dataset
    :param feature_str: the name of the feature to make
    :type feature_str: str
    :returns: function that will accept stuterm_df and engine
    """
    return lambda stuterm_df, engine: rsa_logs_generic(stuterm_df, engine, subtype)


def reenroll_generic(stuterm_df, engine, reen):
    """Generic function to make reenrollment features
    :param stuterm_df: studentid, year, season data
    :param reen: the reenrollment type
                                ['num', 'offpeak', 'pss', 'pns', 'other']
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type reen: str
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame or Series with numeric features
    """
    strats = {'num': {'col': 'entrycomment',
                      'sub_fun': lambda x: 1},
              'off_peak': {'col': 'entrydate',
                           'sub_fun': lambda x: x.month != 8},
              'pss': {'col': 'entrycomment',
                      'sub_fun': lambda x: x == 'Promote Same School'},
              'pns': {'col': 'entrycomment',
                      'sub_fun': lambda x: x == 'Promoted Next School'},
              'other': {'col': 'entrycomment',
                        'sub_fun': lambda x: x != 'Promoted Same School' and\
                        x != 'Promoted Next School'}
              }
    rsql = """select student_number, reenrollment_id,
    current_school, schoolid, entrydate, entrycode,
    entrycomment, exitdate, exitcode, exitcomment
        from clean_data.reenroll"""

    r = pd.read_sql(rsql, engine)

    dateful = r[r['entrydate'].notnull()]
    dateful['season'] = dateful['entrydate'].apply(helpers.season_from_date)
    dateful['measured_year'] = dateful['entrydate'].apply(helpers.ac_year_from_date)
    col = strats[reen]['col']
    sub_fun = strats[reen]['sub_fun']
    dateful['cat'] = dateful[col].apply(sub_fun)
    dateful_minimal = dateful[['student_number', 'measured_year', 'season', 'cat']]
    dateful_stuterm = dateful_minimal.groupby(by=['student_number', 'measured_year', 'season'])\
                                     .agg(sum).reset_index()
    merged_df = stuterm_df.merge(dateful_stuterm,
                                 how='left',
                                 left_on=['studentid', 'measured_year', 'season'],
                                 right_on=['student_number', 'measured_year', 'season'])
    return merged_df['cat']


def make_reenroll_feature(reen_feat):
    """Make features that utilize the reenroll dataset
    :param reen_feat: the name of the feature to make
    :type reen_feat: str
    :returns: function that will accept stuterm_df and engine
    """
    return lambda stuterm_df, engine: reenroll_generic(stuterm_df, engine, reen_feat)


def discipline_generic(stuterm_df, engine, disc):
    """Generic function to make discipline features
    :param stuterm_df: studentid, year, season data
    :param dic: the discipline type
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type reen: str
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame or Series with numeric features
    """
    strats = {'num': {'col': 'incidenttype',
                      'sub_fun': lambda x: 1},
              'disobeyed_rules': {'col': 'incidenttype',
                                  'sub_fun': lambda x: helpers.disc_group(x) == 'disobeyed_rules'},
              'disrespectful_behavior': {'col': 'incidenttype',
                                         'sub_fun': lambda x: helpers.disc_group(x) == 'disrespectful_behavior'},
              'harassment_bullying': {'col': 'incidenttype',
                                      'sub_fun': lambda x: helpers.disc_group(x) == 'harassment_bullying'},
              'no_information': {'col': 'incidenttype',
                                 'sub_fun': lambda x: helpers.disc_group(x) == 'no_information'},
              'skipping_class': {'col': 'incidenttype',
                                 'sub_fun': lambda x: helpers.disc_group(x) == 'skipping_class'},
              'repeated_behavior': {'col': 'incidenttype',
                                    'sub_fun': lambda x: helpers.disc_group(x) == 'repeated_behavior'},
              'disorderly_conduct': {'col': 'incidenttype',
                                     'sub_fun': lambda x: helpers.disc_group(x) == 'disorderly_conduct'},
              'sexual_misconduct': {'col': 'incidenttype',
                                    'sub_fun': lambda x: helpers.disc_group(x) == 'sexual_misconduct'},
              'possess_weapon': {'col': 'incidenttype',
                                 'sub_fun': lambda x: helpers.disc_group(x) == 'possess_weapon'},
              'stealing': {'col': 'incidenttype',
                           'sub_fun': lambda x: helpers.disc_group(x) == 'stealing'},
              'disruptive_conduct': {'col': 'incidenttype',
                                     'sub_fun': lambda x: helpers.disc_group(x) == 'disruptive_conduct'},
              'physical': {'col': 'incidenttype',
                           'sub_fun': lambda x: helpers.disc_group(x) == 'physical'},
              'vandalism': {'col': 'incidenttype',
                            'sub_fun': lambda x: helpers.disc_group(x) == 'vandalism'}
              }
    dem = pd.read_sql_query("SELECT DISTINCT student_number, id FROM clean_data.demographics", engine)
    stuterm_dem_df = stuterm_df.merge(dem, how='left',
                                      left_on=['studentid'],
                                      right_on=['student_number'])
    rsql = """select studentid, incidenttype, incidentdate
        from raw_data.discipline_16_u_of_c_discipline_pk_3rd_data"""

    r = pd.read_sql(rsql, engine)
    r = r[(r['incidentdate'].notnull())]
    r['date'] = r['incidentdate'].apply(lambda x:
                                        datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")\
                                        if len(x) == 19 else None)
    dateful = r[(r['date'].notnull())]
    dateful['season'] = dateful['date'].apply(helpers.season_from_date)
    dateful['measured_year'] = dateful['date'].apply(helpers.ac_year_from_date)
    col = strats[disc]['col']
    sub_fun = strats[disc]['sub_fun']
    dateful['cat'] = dateful[col].apply(sub_fun)
    dateful_minimal = dateful[['studentid', 'season', 'measured_year', 'incidenttype', 'cat']]
    dateful_stuterm = dateful_minimal.groupby(by=['studentid', 'measured_year', 'season'])\
                                     .agg(sum).reset_index()
    merged_df = stuterm_dem_df.merge(dateful_stuterm,
                                     how='left',
                                     left_on=['id', 'measured_year', 'season'],
                                     right_on=['studentid', 'measured_year', 'season'])
    return merged_df['cat']


def make_discipline_feature(disc_feat):
    """Make features that utilize the discipline dataset
    :param disc_feat: the name of the feature to make
    :type disc_feat: str
    :returns: function that will accept stuterm_df and engine
    """
    return lambda stuterm_df, engine: discipline_generic(stuterm_df, engine, disc_feat)


def rsa_summer_enrolled(stuterm_df, engine):
    """
    Returns indicator whether or not student was enrolled in RSA in a particular year 
    (only available for 2014 and 2015)
    :param stuterm_df: studentid, year, season data
    :param engine: a db engine to use
    :type stuterm_df: pandas DataFrame
    :type engine: sqlalchemy engine
    :returns: pandas DataFrame int where 1 = was enrolled
    """
    rsa_feature = pd.read_sql_query("SELECT * from clean_data.rsa_summer", engine)
    rsa_feature.loc[rsa_feature['course_number'].isnull(), 'course_number'] = ""
    dem = pd.read_sql_query("SELECT student_number, id, measured_year, grade_level FROM clean_data.demographics", engine)
    stuterm_dem_df = stuterm_df.merge(dem, how='left',
                                      left_on=['studentid', 'measured_year'],
                                      right_on=['student_number', 'measured_year'])
    stuterm_dem_df_14 = stuterm_dem_df[stuterm_dem_df['measured_year']!="15_16"]
    stuterm_dem_df_15 = stuterm_dem_df[stuterm_dem_df['measured_year']=="15_16"]
    stuterm_rsa_df_14 = stuterm_dem_df_14.merge(rsa_feature, how='left',
                                                left_on=['studentid', 'measured_year'],
                                                right_on=['id', 'measured_year'])
    stuterm_rsa_df_15 = stuterm_dem_df_15.merge(rsa_feature, how='left',
                                                left_on=['id', 'measured_year'],
                                                right_on=['id', 'measured_year'])
    st_rsa_14 = stuterm_rsa_df_14.drop(['id_x', 'id_y'], axis=1)
    st_rsa_15 = stuterm_rsa_df_15.drop('id', axis=1)
    st_rsa = st_rsa_14.append(st_rsa_15)
    st_rsa['rsa_summer_is_enrolled'] = np.nan
    st_rsa.loc[st_rsa['course_number'].notnull(), 'rsa_summer_is_enrolled'] = 1
    rsa_enrolled = st_rsa['rsa_summer_is_enrolled'].reset_index()
    return rsa_enrolled.iloc[:, 1]


def tfa_summer_enrolled(stuterm_df, engine):
    """
    Generates TFA summer school enrollment feature for that
    measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: TFA summer school binary enrollment feature
    :rtype: pandas DataFrame
    """
    tfa_sql = """
              WITH tfa_enroll AS (
                   SELECT
                       student_number,
                       1 AS enrolled,
                       measured_year
                   FROM
                       clean_data.tfa
               )

               SELECT
                   *,
                   'fall' AS season
               FROM
                   tfa_enroll

               UNION ALL

               SELECT
                   *,
                   'winter' AS season
               FROM
                   tfa_enroll

               UNION ALL

               SELECT
                   *,
                   'spring' AS season
               FROM
                   tfa_enroll;
               """
    tfa_df = pd.read_sql_query(tfa_sql, engine)
    stuterm_tfa_df = stuterm_df.merge(tfa_df[['measured_year',
                                              'student_number',
                                              'season',
                                              'enrolled']],
                                      how='left',
                                      left_on=['studentid',
                                               'measured_year',
                                               'season'],
                                      right_on=['student_number',
                                                'measured_year',
                                                'season'])
    return stuterm_tfa_df['enrolled']


def tfa_summer_days_enrolled(stuterm_df, engine):
    """
    Generates number of days enrolled in TFA summer school
    for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: TFA summer school days enrolled feature
    :rtype: pandas DataFrame
    """
    tfa_sql = """
              WITH tfa_enroll AS (
                   SELECT
                       student_number,
                       CAST(EXTRACT(EPOCH FROM exit_date - entry_date) AS INT)
                           /(60*60*24) AS days_enrolled,
                       measured_year
                   FROM
                       clean_data.tfa
               ),
               mean_days AS (
                   SELECT
                      AVG(days_enrolled) AS mean_enrollment
                   FROM
                       tfa_enroll
                   WHERE
                       days_enrolled > 0
               )

               SELECT
                   student_number,
                   measured_year,
                   CASE WHEN days_enrolled > 0
                      THEN days_enrolled
                      ELSE (SELECT mean_enrollment FROM mean_days)
                   END AS days_enrolled,
                   'fall' AS season
               FROM
                   tfa_enroll

               UNION ALL

               SELECT
                   student_number,
                   measured_year,
                   CASE WHEN days_enrolled > 0
                      THEN days_enrolled
                      ELSE (SELECT mean_enrollment FROM mean_days)
                   END AS days_enrolled,
                   'winter' AS season
               FROM
                   tfa_enroll

               UNION ALL

               SELECT
                   student_number,
                   measured_year,
                   CASE WHEN days_enrolled > 0
                      THEN days_enrolled
                      ELSE (SELECT mean_enrollment FROM mean_days)
                   END AS days_enrolled,
                   'spring' AS season
               FROM
                   tfa_enroll;
               """
    tfa_df = pd.read_sql_query(tfa_sql, engine)
    stuterm_tfa_df = stuterm_df.merge(tfa_df[['measured_year',
                                              'student_number',
                                              'season',
                                              'days_enrolled']],
                                      how='left',
                                      left_on=['studentid',
                                               'measured_year',
                                               'season'],
                                      right_on=['student_number',
                                                'measured_year',
                                                'season'])

    return stuterm_tfa_df['days_enrolled']


def tfa_teacher(stuterm_df, engine):
    """
    Generates the TFA teacher name for that measured year

    :param stuterm_df: studentid, year, season data
    :type stuterm_df: pandas DataFrame
    :param engine: a db engine to use
    :type engine: sqlalchemy engine

    :returns: TFA summer school teacher name feature
    :rtype: pandas DataFrame
    """
    tfa_teacher_sql = """
                      WITH tfa_enroll AS (
                          SELECT
                              student_number,
                              teacher_name,
                              measured_year
                          FROM
                              clean_data.tfa
                      )

                      SELECT
                          *,
                          'fall' AS season
                      FROM
                          tfa_enroll

                      UNION ALL

                      SELECT
                          *,
                          'winter' AS season
                      FROM
                          tfa_enroll

                      UNION ALL

                      SELECT
                          *,
                          'spring' AS season
                      FROM
                          tfa_enroll;
                      """
    tfa_teacher_df = pd.read_sql_query(tfa_teacher_sql, engine)
    stuterm_tfa_teacher_df = stuterm_df.merge(tfa_teacher_df[['measured_year',
                                                              'student_number',
                                                              'season',
                                                              'teacher_name']],
                                              how='left',
                                              left_on=['studentid',
                                                       'measured_year',
                                                       'season'],
                                              right_on=['student_number',
                                                        'measured_year',
                                                        'season'])
    return stuterm_tfa_teacher_df['teacher_name']


def get_att_sql(att_col_name, att_code):
    """
    SQL shell for demographics data. If feature is static, then
    most recent record is applied for that student.

    :param att_col_name: name of feature to be reflected in later DataFrame
    :type dem_col: str
    :param att_code: code of attendance feature in attendance table
    :type static: str

    :returns: full sql statement
    :rtype: str
    """
    att_sql = """
              WITH dem AS (
                  SELECT
                      DISTINCT id,
                      student_number
                  FROM
                      clean_data.demographics
              ),
              att AS (
                SELECT
                    att_by_day_12_16.*,
                    dem.student_number
                FROM
                    clean_data.att_by_day_12_16
                    INNER JOIN dem
                        ON (att_by_day_12_16.studentid = dem.id)
                WHERE
                  att_code = '{code}'
              ),
              map_season_date AS (
                SELECT
                    DISTINCT measured_year,
                    season,
                    CASE season
                        WHEN 'fall'
                            THEN TO_DATE('20' || map.cal_year || '-08-01',
                                         'YYYY-MM-DD')
                        WHEN 'winter'
                            THEN TO_DATE('20' || map.cal_year || '-01-01',
                                         'YYYY-MM-DD')
                        WHEN 'spring'
                            THEN TO_DATE('20' || map.cal_year || '-03-01',
                                         'YYYY-MM-DD')
                    END season_start,
                    CASE season
                        WHEN 'fall'
                            THEN TO_DATE('20' || map.cal_year+1 || '-01-01',
                                         'YYYY-MM-DD')
                        WHEN 'winter'
                            THEN TO_DATE('20' || map.cal_year || '-03-01',
                                         'YYYY-MM-DD')
                        WHEN 'spring'
                            THEN TO_DATE('20' || map.cal_year || '-08-01',
                                         'YYYY-MM-DD')
                    END season_end
                FROM
                    clean_data.map
              )

              SELECT
                map_season_date.measured_year,
                map_season_date.season,
                att.student_number,
                COUNT(*) AS {col_name}
              FROM
                att
                INNER JOIN map_season_date
                    ON (att.att_date >= map_season_date.season_start
                        AND att.att_date < map_season_date.season_end)
              GROUP BY
                measured_year,
                season,
                student_number;
                """.format(col_name=att_col_name, code=att_code)
    return att_sql


def make_attendance_feature(att_code, att_col_name):
    """Make features that utilize the attendance dataset
    :param feature_str: the name of the feature to make
    :type feature_str: str
    :returns: function that will accept stuterm_df and engine
    """
    return lambda stuterm_df, engine: att_feature(stuterm_df, engine,
                                                  att_code, att_col_name)


def att_feature(stuterm_df, engine, att_code, att_col_name):
    """
    Generates attendance metrics per term for each student

    :param att_code: code in attendance table for that att feature
    :type att_code: str
    :param att_col_name: column name for that attendance feature
    :type att_col_name: str

    :returns: attendance feature
    :rtype: pandas DataFrame
    """
    att_sql = get_att_sql(att_col_name, att_code)
    att_df = pd.read_sql_query(att_sql, engine)
    stuterm_att_df = stuterm_df.merge(att_df, how='left',
                                      left_on=['studentid',
                                               'measured_year',
                                               'season'],
                                      right_on=['student_number',
                                                'measured_year',
                                                'season'])
    return stuterm_att_df[att_col_name]


def map_max_score(stuterm_df, engine):
    stuterm_df_copy = stuterm_df
    stuterm_df_copy['map_testritscore'] = make_feature_from_str('map_testritscore', engine, stuterm_df)
    stuterm_df_copy['season_order'] = stuterm_df_copy['season'].apply(lambda x:{'fall': 1, 'winter': 2, 'spring': 3}[x])
    max_scores = stuterm_df_copy.sort_values(['studentid', 'measured_year', 'season_order'])\
                                .groupby('studentid').apply(max_score_to_date).reset_index()
    stuterm_df_copy = stuterm_df_copy.reset_index().merge(max_scores, how='left',
                                                          left_on=stuterm_df_copy.reset_index()['index'],
                                                          right_on=max_scores['level_1'])
    return stuterm_df_copy['max_score']


def max_score_to_date(df):
    df['max_score'] = df['map_testritscore']
    for (prev_index, prev_row), (this_index, this_row) in helpers.pairwise(df.iterrows()):
        if len(df) == 1:
            pass
        elif this_row['map_testritscore'] > df.loc[prev_index, 'max_score']:
            df.loc[this_index, 'max_score'] = df.loc[this_index, 'map_testritscore']
        else:
            df.loc[this_index, 'max_score'] = df.loc[prev_index, 'max_score']
    return df['max_score']


def num_consecutive_negs(df):
    df['num_consecutive_negs'] = 0
    df.ix[df.index[0], 'num_consecutive_negs'] = int(df.ix[df.index[0], 'diffs'] < 0)
    for (prev_index, prev_row), (this_index, this_row) in helpers.pairwise(df.iterrows()):
        if this_row['diffs'] < 0:
            df.loc[this_index, 'num_consecutive_negs'] = df.loc[prev_index, 'num_consecutive_negs'] +1
    return df['num_consecutive_negs']


def map_derived_feature(feature_type, stuterm_df, engine):
    """Generates differences between successive map scores
    :param
    :type
    :returns:
    """
    stuterm_df['map_testritscore'] = make_feature_from_str('map_testritscore',
                                                           engine, stuterm_df)
    idx = stuterm_df.index
    stuterm_df.sort_values(['studentid', 'measured_year', 'season'], inplace=True)
    stuterm_df['diffs'] = stuterm_df['map_testritscore'].diff()
    mask = stuterm_df.studentid != stuterm_df.studentid.shift(1)
    idx_mask = mask.index.tolist()
    stuterm_df.loc[idx_mask, 'diffs'] = np.nan
    stuterm_df = stuterm_df.reindex(idx)
    if feature_type == 'diff':
        return stuterm_df['diffs']
    elif feature_type == 'total_diff':
        first_map = stuterm_df.sort_values(['studentid',
                                            'measured_year',
                                            'season']).groupby('studentid').first()['map_testritscore'].reset_index()
        first_map.columns = ['studentid', 'first_map']
        stuterm_df = stuterm_df.merge(first_map, how='left',
                                      left_on='studentid', 
                                      right_on='studentid')
        stuterm_df['total_diff'] = stuterm_df['map_testritscore'] - stuterm_df['first_map']
        return stuterm_df['total_diff']
    elif feature_type == 'year_diff':
        year_diff = stuterm_df.sort_values(['studentid',
                                            'measured_year',
                                            'season']).groupby(['studentid',
                                                                'measured_year']).last()['map_testritscore'] \
            - stuterm_df.sort_values(['studentid',
                                      'measured_year',
                                      'season']).groupby(['studentid',
                                                          'measured_year']).first()['map_testritscore']
        year_diff = year_diff.reset_index()
        year_diff.columns = ['studentid', 'measured_year', 'year_diff']
        stuterm_df = stuterm_df.merge(year_diff, how='left',
                                      left_on=['studentid', 'measured_year'],
                                      right_on=['studentid', 'measured_year'])
        return stuterm_df['year_diff']
    elif feature_type == 'std':
        stds = stuterm_df.groupby('studentid')['diffs'].apply(np.nanstd).reset_index()
        stds.columns = ['studentid', 'std']
        stuterm_df = stuterm_df.merge(stds, how='left',
                                      left_on= 'studentid',
                                      right_on='studentid')
        return stuterm_df['std']
    elif feature_type == 'num_tests':
        num_tests = stuterm_df.groupby(['studentid',
                                        'measured_year',
                                        'season']).count().groupby(level=[0]).cumsum()['map_testritscore'].reset_index()
        num_tests.columns = ['studentid', 'measured_year', 'season', 'number_tests_taken']
        stuterm_df = stuterm_df.merge(num_tests, how='left',
                                      left_on=['studentid', 'measured_year', 'season'],
                                      right_on=['studentid', 'measured_year', 'season'])
        return stuterm_df['number_tests_taken']
    elif feature_type == 'num_tests_term':
        map_col = "testritscore"
        where_statement = "where discipline = 'Reading'"
        map_select_sql = """select {map_col}, studentid, measured_year, season
                    from clean_data.map {where_statement}""".format(map_col=map_col, where_statement=where_statement)
        map_col_df = pd.read_sql_query(map_select_sql, engine)
        test_counts = map_col_df.groupby(['studentid',
                                          'measured_year',
                                          'season']).count()['testritscore'].reset_index()
        test_counts.columns = ['studentid', 'measured_year', 'season', 'number_tests_term']
        stuterm_df = stuterm_df.merge(test_counts, how='left',
                                      left_on=['studentid', 'measured_year', 'season'],
                                      right_on=['studentid', 'measured_year', 'season'])
        return stuterm_df['number_tests_term']
    elif feature_type == 'num_consecutive_negs':
        cons_negs = stuterm_df.sort_values(['studentid',
                                            'measured_year',
                                            'season'])\
                              .groupby('studentid').apply(num_consecutive_negs).reset_index()
        stuterm_df = stuterm_df.reset_index().merge(cons_negs, how='left',
                                                    left_on=stuterm_df.reset_index()['index'],
                                                    right_on=cons_negs['level_1'])
        return stuterm_df['num_consecutive_negs']


def make_map_feature_derived(feature_str):
    return lambda stuterm_df, engine: map_derived_feature(feature_str, stuterm_df, engine)

feat_fun = {
    'female': female_feature,
    'eventual186': stuterm_labels_eventual_not_186(3, True),
    'eventualnot186': stuterm_labels_eventual_not_186(3),
    'eventualnot186_with2nd': stuterm_labels_eventual_not_186(2),
    'eventualnot186_omitpassing': stuterm_labels_eventual_not_186_omit_passing(2),
    'eventual186_omitpassing': stuterm_labels_eventual_186_omit_passing(2, True),
    'map_testritscore': make_map_feature('map_testritscore'),
    'map_testpercentile': make_map_feature('map_testpercentile'),
    'map_testdurationminutes': make_map_feature('map_testdurationminutes'),
    'map_percentcorrect': make_map_feature('map_percentcorrect'),
    'map_start_date': make_map_feature('map_start_date'),
    'map_start_hour': make_map_feature('map_start_hour'),
    'map_season': map_season,
    'map_reading_testritscore': make_map_feature('map_reading_testritscore'),
    'map_reading_testpercentile': make_map_feature('map_reading_testpercentile'),
    'map_reading_testdurationminutes': make_map_feature('map_reading_testdurationminutes'),
    'map_reading_percentcorrect': make_map_feature('map_reading_percentcorrect'),
    'map_reading_start_date': make_map_feature('map_reading_start_date'),
    'map_reading_start_hour': make_map_feature('map_reading_start_hour'),
    'tripod_challenge_min': make_tripod_feature('tripod_challenge_min'),
    'tripod_challenge_max': make_tripod_feature('tripod_challenge_max'),
    'tripod_challenge_mean': make_tripod_feature('tripod_challenge_mean'),
    'tripod_challenge_std': make_tripod_feature('tripod_challenge_std'),
    'tripod_classroom_management_min': make_tripod_feature('tripod_classroom_management_min'),
    'tripod_classroom_management_max': make_tripod_feature('tripod_classroom_management_max'),
    'tripod_classroom_management_mean': make_tripod_feature('tripod_classroom_management_mean'),
    'tripod_classroom_management_std': make_tripod_feature('tripod_classroom_management_std'),
    'tripod_captivate_min': make_tripod_feature('tripod_captivate_min'),
    'tripod_captivate_max': make_tripod_feature('tripod_captivate_max'),
    'tripod_captivate_mean': make_tripod_feature('tripod_captivate_mean'),
    'tripod_captivate_std': make_tripod_feature('tripod_captivate_std'),
    'tripod_care_min': make_tripod_feature('tripod_care_min'),
    'tripod_care_max': make_tripod_feature('tripod_care_max'),
    'tripod_care_mean': make_tripod_feature('tripod_care_mean'),
    'tripod_care_std': make_tripod_feature('tripod_care_std'),
    'tripod_clarify_min': make_tripod_feature('tripod_clarify_min'),
    'tripod_clarify_max': make_tripod_feature('tripod_clarify_max'),
    'tripod_clarify_mean': make_tripod_feature('tripod_clarify_mean'),
    'tripod_clarify_std': make_tripod_feature('tripod_clarify_std'),
    'tripod_consolidate_min': make_tripod_feature('tripod_consolidate_min'),
    'tripod_consolidate_max': make_tripod_feature('tripod_consolidate_max'),
    'tripod_consolidate_mean': make_tripod_feature('tripod_consolidate_mean'),
    'tripod_consolidate_std': make_tripod_feature('tripod_consolidate_std'),
    'tripod_confer_min': make_tripod_feature('tripod_confer_min'),
    'tripod_confer_max': make_tripod_feature('tripod_confer_max'),
    'tripod_confer_mean': make_tripod_feature('tripod_confer_mean'),
    'tripod_confer_std': make_tripod_feature('tripod_confer_std'),
    'tripod_cs_min': make_tripod_feature('tripod_cs_min'),
    'tripod_cs_max': make_tripod_feature('tripod_cs_max'),
    'tripod_cs_mean': make_tripod_feature('tripod_cs_mean'),
    'tripod_cs_std': make_tripod_feature('tripod_cs_std'),
    'course_taken_art': make_course_feature('course', 'art'),
    'course_taken_pe': make_course_feature('course', 'pe'),
    'course_taken_read': make_course_feature('course', 'read'),
    'course_taken_science': make_course_feature('course', 'science'),
    'course_taken_math': make_course_feature('course', 'math'),
    'course_taken_social': make_course_feature('course', 'social'),
    'course_taken_computer': make_course_feature('course', 'computer'),
    'course_taken_non_grade': make_course_feature('course', 'non_grade'),
    'course_taken_language': make_course_feature('course', 'language'),
    'grade_mark_a': make_course_feature('grade', 'a'),
    'grade_mark_b': make_course_feature('grade', 'b'),
    'grade_mark_c': make_course_feature('grade', 'c'),
    'grade_mark_d': make_course_feature('grade', 'd'),
    'grade_mark_f': make_course_feature('grade', 'f'),
    'grade_mark_s': make_course_feature('grade', 's'),
    'grade_mark_n': make_course_feature('grade', 'n'),
    'grade_mark_u': make_course_feature('grade', 'u'),
    'grade_mark_e': make_course_feature('grade', 'e'),
    'grade_mark_p': make_course_feature('grade', 'p'),
    'grade_mark_ng': make_course_feature('grade', 'ng'),
    'rsa_log_rsa_retained': make_rsa_log_feature('RSA_RETAINED'),
    'rsa_log_passed_itbs': make_rsa_log_feature('PASSED_ITBS'),
    'rsa_log_probation_promoted': make_rsa_log_feature('PROBATION_PROMOTED'),
    'rsa_log_passed_occt': make_rsa_log_feature('PASSED_OCCT'),
    'rsa_log_exemption': make_rsa_log_feature('EXEMPTION'),
    'rsa_log_meets_rsa_criteria': make_rsa_log_feature('MEETS_RSA_CRITERIA'),
    'iread_is_enrolled': iread_enrolled,
    'iread_data_missing': iread_data_missing,
    'iread_took_screener': iread_took_screener,
    'iread_average_time_per_topic': iread_average_time_per_topic,
    'iread_average_sessions_per_week': iread_average_sessions_per_week,
    'iread_current_series': make_iread_current_series_topic('series'),
    'iread_current_topic': make_iread_current_series_topic('topic'),
    'iread_screener_placement_series': make_iread_feature('iread_screener_placement_series'),
    'iread_highest_unit_reached': make_iread_feature('iread_highest_unit_reached'),
    'iread_total_sessions': make_iread_feature('iread_total_sessions'),
    'iread_total_topics_completed': make_iread_feature('iread_total_topics_completed'),
    'iread_total_time': make_iread_feature('iread_total_time'),
    'ethnicity': ethnicity_feature,
    'age': age_feature,
    'ell': ell_feature,
    'ell_language': ell_lang_feature,
    'disability_code': disability_code_feature,
    'service_delivery': service_delivery_feature,
    'lunch_status': lunch_feature,
    'homeless': homeless_feature,
    'lives_with': lives_with_feature,
    'school': school_feature,
    'reenroll_num': make_reenroll_feature('num'),
    'reenroll_off_peak': make_reenroll_feature('off_peak'),
    'reenroll_pss': make_reenroll_feature('pss'),
    'reenroll_pns': make_reenroll_feature('pns'),
    'reenroll_other': make_reenroll_feature('other'),
    'discipline_num': make_discipline_feature('num'),
    'discipline_disobeyed_rules': make_discipline_feature('disobeyed_rules'), 
    'discipline_disrespectful_behavior': make_discipline_feature('disrespectful_behavior'),
    'discipline_harassment_bullying': make_discipline_feature('harassment_bullying'),
    'discipline_no_information': make_discipline_feature('no_information'),
    'discipline_skipping_class': make_discipline_feature('skipping_class'),
    'discipline_repeated_behavior': make_discipline_feature('repeated_behavior'),
    'discipline_disorderly_conduct': make_discipline_feature('disorderly_conduct'),
    'discipline_sexual_misconduct': make_discipline_feature('sexual_misconduct'),
    'discipline_possess_weapon': make_discipline_feature('possess_weapon'), 
    'discipline_stealing': make_discipline_feature('stealing'),
    'discipline_disruptive_conduct': make_discipline_feature('disruptive_conduct'),
    'discipline_physical': make_discipline_feature('physical'),
    'discipline_vandalism': make_discipline_feature('vandalism'),
    'rsa_summer_enrolled': rsa_summer_enrolled,
    'rsa_summer_school': rsa_summer_enrolled,
    'att_tardiness': make_attendance_feature('tardy', 'att_tardiness'),
    'att_absence': make_attendance_feature('absent', 'att_absence'),
    'att_with_explanation': make_attendance_feature('with explanation', 'att_with_explanation'),
    'att_other': make_attendance_feature('other', 'att_other'),
    'att_excused_absence': make_attendance_feature('excused', 'att_excused_absence'),
    'att_unexcused_absence': make_attendance_feature('unexcused', 'att_unexcused_absence'),
    'att_leave_early': make_attendance_feature('leaves early', 'att_leave_early'),
    'att_school_activity': make_attendance_feature('school activity', 'att_school_activity'),
    'att_nurse': make_attendance_feature('nurse', 'att_nurse'),
    'att_half_day_absence': make_attendance_feature('half day absent', 'att_half_day_absence'),
    'att_in_school_suspension': make_attendance_feature('in-school suspension', 'att_in_school_suspension'),
    'att_truancy': make_attendance_feature('truancy', 'att_truancy'),
    'att_counselor': make_attendance_feature('counselor', 'att_counselor'),
    'att_administrator': make_attendance_feature('administrator', 'att_administrator'),
    'tfa_summer_enrolled': tfa_summer_enrolled,
    'tfa_summer_days_enrolled': tfa_summer_days_enrolled,
    'tfa_teacher': tfa_teacher,
    'map_max_score': map_max_score,
    'map_diff': make_map_feature_derived('diff'),
    'map_total_diff': make_map_feature_derived('total_diff'),
    'map_year_diff': make_map_feature_derived('year_diff'),
    'map_std': make_map_feature_derived('std'),
    'map_num_tests': make_map_feature_derived('num_tests'),
    'map_num_tests_term': make_map_feature_derived('num_tests_term'),
    'map_num_consecutive_negs': make_map_feature_derived('num_consecutive_negs')
}


def make_feature_from_str(feature_str, engine, stuterm_df):
    return feat_fun[feature_str](stuterm_df, engine)
