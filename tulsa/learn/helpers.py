import logging
import os
from itertools import tee

def termid_to_ac_year(termid):
    """produces an str academic year in the form YY_YY+1
    from a 4 digit termid, or 'nan' if invalid termid

    :param termid: the termid to convert
    :type termid: int
    :returns: str
    """
    str_termid = str(termid)
    if not len(str_termid) == 4:
        return float('nan')
    else:
        key_year = int(str_termid[1])
        return '1{}_1{}'.format(key_year, key_year+1)


def categorize_courses(course_name):
    """categorize popular classes into 10 major categories

    :param course_name: the course name to categorize
    :type course_name: str
    :returns: str
    """
    courses_cat = {'P E': 'pe',
                   'MUSIC': 'art',
                   'ART': 'art',
                   'GR 1 SCIENCE': 'science',
                   'GR 1 SOCST': 'social',
                   'GR 1 MATH': 'math',
                   'GR 1 READ': 'read',
                   'GR 2 READ': 'read',
                   'GR 2 SOCST': 'social',
                   'GR 2 MATH': 'math',
                   'GR 2 SCIENCE': 'science',
                   'GR 3 MATH': 'math',
                   'GR 3 READ': 'read',
                   'GR 3 SCIENCE': 'science',
                   'GR 3 SOCST': 'social',
                   'COMPUTER': 'computer',
                   'WDN GRADES ONLY': 'non_grade',
                   'LIBRARY SKILLS': 'read',
                   'NO GRADES EARNED': 'non_grade',
                   'GR 2 READ (SPANISH)': 'language',
                   'GR 1 READ (SPANISH)': 'language',
                   'SPANISH': 'language',
                   'FRENCH': 'language',
                   'GR 3 READ (SPANISH)': 'language',
                   'SPANISH READING': 'language'}
    try:
        return courses_cat[course_name]
    except KeyError:
        return 'non-grade'


def categorize_grades(grade):
    """categorize grades into standard grades or non

    :param grade: the grade name to normalize
    :type grade: str
    :returns: str
    """
    valid_grades = frozenset(['a', 'b', 'c', 'd',
                              'e', 'f', 's', 'n',
                              'u', 'p', 'ng'])
    if grade:
        grade = grade.lower()
        if grade in valid_grades:
            return grade
    # either no grade, or grade not a valid grade
    return 'non_standard_grade'


def season_from_date(date):
    """"fall", "winter", or "spring" given a timestamp obj
    :param date: the date to classify
    :type date: datetime.datetime
    :returns: str
    """
    month = date.month
    if month >= 8 and month < 13:
        season = 'fall'
    elif month >= 0 and month < 3:
        season = 'winter'
    elif month >= 3 and month < 8:
        season = 'spring'
    return season


def ac_year_from_date(date):
    """produces an str academic year in the form YY_YY+1

    :param date: the date to classify
    :type date: datetime.datetime
    :returns: str
    """
    season = season_from_date(date)
    if season == 'fall':
        start_year, end_year = date.year, date.year + 1
    elif season in ('spring', 'winter'):
        start_year, end_year = date.year - 1, date.year
    start_year_2dig = str(start_year)[2:]
    end_year_2dig = str(end_year)[2:]
    return '{}_{}'.format(start_year_2dig, end_year_2dig)


def alter_features_add_column(from_table, from_col, to_table, engine):
    """
    Copies column from_col from table from_talbe to to_table
    matching on stuterms
    :param from_table: the features table to copy from
    :param to_table: the features table to copy to
    :param from_col: the column name in from_table to copy
    :param engine: the engine to use
    :param from_table: str
    :param to_table: str
    :param from_col: str
    :param engine: sqlalchemy engine
    """
    col_type_sql = """SELECT data_type
                      FROM information_schema.columns
                      WHERE table_schema = 'features'
                        AND table_name = '{from_table}'
                        AND column_name = '{from_col}'
                        """.format(from_table=from_table,
                                   from_col=from_col)
    col_type = engine.execute(col_type_sql).fetchone()[0]

    alter_sql = """alter table features.{to_table}
                    add column {from_col} {col_type}
                """.format(from_col=from_col,
                           to_table=to_table,
                           col_type=col_type)

    engine.execute(alter_sql)

    update_sql = """UPDATE features.{to_table}
                    SET {from_col} = features.{from_table}.{from_col}
                    FROM features.{from_table}
                    WHERE features.{to_table}.studentid = features.{from_table}.studentid
                        AND features.{to_table}.measured_year = features.{from_table}.measured_year
                        AND features.{to_table}.season = features.{from_table}.season
                        """.format(from_table=from_table,
                                   from_col=from_col,
                                   to_table=to_table)

    engine.execute(update_sql)


def get_next_ver_number(item_name, state_location, extension=None):
    """
    looks into the filesystem to get the highest numbered +1
    of an 'item_name_number' file.
    :param item_name: the prefix of the file name before num
    :type item_name: str
    :param extension: the extension associated with the files
    :type extension: str
    :param state_location: the dir where the files live
    :type state_location: str
    :returns str: next number
    """
    ls = os.listdir(state_location)
    rel_files = [f for f in ls if f.startswith(item_name)]
    # check to see if any relevant files exists yet
    if rel_files:
        if extension:
            rel_files = [f.split(extension)[0] for f in rel_files]
        past_nums = [int(f.split('_')[-1]) for f in rel_files]
        recentest = max(past_nums)
        next_num = recentest + 1
    else:  # no rel files yet
        next_num = 0
    return next_num


def save_fig(plt, model_name, fig_dir):
    """
    save fig of plt with filename from model_name
    at fig_dir
    :param plt: a plot
    :type plt: matplotlibplot
    :param model_name: model name
    :type model_name: str
    :param fig_dir: the directory to save in
    :type fig_dir: str
    :returns str: the filepath saved
    """
    fig_num = get_next_ver_number(model_name, fig_dir, '.png')
    filepath = '{}/{}_{}'.format(fig_dir, model_name, fig_num)
    plt.savefig(filepath)
    plt.close()
    return filepath


def touch_run_number(run_name, run_number, state_location):
    """
    touch a file keep track of runs
    :param run_name:
    :param run_number:
    :param state_location:
    """
    fname = '{}/{}_{}'.format(state_location, run_name, run_number)
    with open(fname, 'a'):
        os.utime(fname, times=None)


def disc_group(disc):
    """function that categorises discipline incidents
    :param disc: raw discipline category
    :returns: string, new discipline category
    """
    disc_cat_dict = {'disruptive_conduct': ['214 DISRUPTIVE CONDUCT',
                                            '414 FALSE ALARM'],
                     'physical': ['211 FIGHTING',
                                  '210 UNACCEPTABLE MINOR PHYSICAL CONTACT', '300 FIGHTING (15-16 SY)',
                                  '210 ENGAGING IN INAPPROPRIATE OR UNWANTED PHYSICAL CONTACT',
                                  '314 ASSAULT (15-16 SY)',
                                  '408 PHYSICAL ASSAULT OF STAFF',
                                  '406 ASSAULT',
                                  '407 BATTERY',
                                  '408 ASSAULT OR BATTERY ON STAFF'],
                     'disobeyed_rules': ['109 FAILURE TO FOLLOW CLASS RULES',
                                         '106 INSUBORDINATION', '213 BUS RULES',
                                         '220 REFUSAL TO SERVE MINOR SANCTIONS',
                                         '109 FAILURE TO FOLLOW CLASSROOM RULES',
                                         '218 LEAVING CAMPUS W/O PERMISSION',
                                         '218 LEAVING W/O PERMISSION',
                                         '217 TRUANCY',
                                         '110 ACADEMIC DISHONESTY/CHEATING'],
                     'disorderly_conduct': ['302 DISORDERLY CONDUCT',
                                            '201 INAPPROPRIATE USE OF TECH/COMPUTERS',
                                            '102 INAPPROPRIATE PERSONAL PROPERTY',
                                            '203 SMOKING OR USE OF SMOKELESS TOBACCO OR E-CIGARETTES'],
                     'disrespectful_behavior': ['108 DISRESPECT',
                                                '306 ABUSIVE BEHAVIOR TO SCHOOL PERSONNEL',
                                                '107 VERBAL/NON-VERBAL PROFANITY',
                                                '305 VERBAL ABUSE TO STAFF',
                                                '417 DISREGARD FOR HEALTH/SAFETY-OTHER',
                                                '305 VERBAL ABUSE STAFF'],
                     'harassment_bullying': ['219 HARASSMENT, INTIMIDATION, OR THREATENING BEHAVIOR (SINGLE INCIDENT)',
                                             '202 BULLYING',
                                             '219 HARASSMENT, INTIMIDATION, OR THREATENING BEHAVIOR',
                                             '202 HARRASS/INTIMIDATE/BULLY',
                                             '306 ABUSIVE BEHAVIOR',
                                             '409 THREAT WITH INTENT TO KILL'],
                     'skipping_class': '215 SKIPPING/CUTTING CLASS',
                     'no_information': ['0', ''],
                     'possess_weapon': ['402 POSSESS WEAPON/FACSIMILE',
                                        '301 POSSESS OF MACE/CHEMICAL AGENTS/ETC',
                                        '405 THREAT WITH DANGEROUS WEAPON'],
                     'repeated_behavior': ['204 EXCESSIVE REFERRALS',
                                           '200 PERSISTENT VIOLATION OF 100 LEVEL BEHAVIORS',
                                           '200 PERSISTENT VIOLATION OF 100 LEVEL TB'],
                     'stealing': ['207 POSSESS STOLEN PROP', '310 THEFT BY RECEIVING'],
                     'sexual_misconduct': ['210 SEXUAL MISCONDUCT',
                                           '316 SEXUAL HARASSMENT',
                                           '419 SEXUAL-RELATED OFFENSES'],
                     'vandalism': ['311 B & E/VANDALISM >$500',
                                   '311 B & E/VANDALISM',
                                   '403 ARSON']}
    result = 'other'
    if disc is None:
        pass
    else:
        for key, value in disc_cat_dict.items():
            if disc in value:
                result = key
    return result


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)