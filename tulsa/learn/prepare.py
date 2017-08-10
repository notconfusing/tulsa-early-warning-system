from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import MinMaxScaler
from tulsa.etl.sql_str_normer import normalize_name_generic

import pandas as pd
import numpy as np


def impute_zeros(col, stuterm_df):
    """return col, but with 0s instead of NaNs
    :param col: the column to impute zeros on
    :param stuterm_df: the index to match to if needed
    :type col: pandas Series
    :type stuterm_df: pandas DataFrame
    :returns: pandas Series
    """
    zeroed_col = col.fillna(value=0)
    return zeroed_col


def impute_iden(col, stuterm_df):
    """return col as is, because it should have no NaNs
    should return an error.
    :param col: the column
    :param stuterm_df: the index
    :type col: pandas Series
    :type stuterm_df: pandas DataFrame
    :returns: pandas Series
    """
    return col


def impute_fun(col, fun):
    """return col, but with fun applied to NaN entries, 
    :param col: the column to impute fun on
    :param fun: function to use, "mean", "media", or "most_frequent"
    :type col: pandas Series
    :type fun: str
    :returns: pandas Series
    """
    # sk learn is not happy about 1-d DataFrames
    noninf_col = col.replace([np.inf, -np.inf], np.nan)
    np_rep = noninf_col.reshape(-1, 1)
    imp = Imputer(missing_values='NaN', strategy=fun)
    imp.fit(np_rep)
    transformed = imp.transform(np_rep)
    return transformed


def impute_mean(col, stuterm_df):
    """return col, but with mean, 
    :param col: the column to impute fun on
    :param stuterm_df: the index to match to if needed
    :param fun: function to use, "mean", "media", or "most_frequent"
    :type col: pandas Series
    :type stuterm_df: pandas DataFrame
    :type fun: str
    :returns: pandas Series
    """
    col_title = col.name
    imputed = impute_fun(col, 'mean')
    named_imputed = pd.DataFrame(imputed, columns=[col_title])
    return named_imputed


def cat_binarizer(col, stuterm_df):
    col_title = col.name
    lb = LabelBinarizer()
    col_missing = col.fillna(value='missing')
    col_missing = col_missing.apply(lambda x: str(x))
    lb.fit(col_missing)
    transformed = lb.transform(col_missing)
    normed_col_names = [normalize_name_generic(col_name, False) for
                        col_name in lb.classes_]
    titled_col_names = ['{}___{}'.format(col_title, norm_name) for
                        norm_name in normed_col_names]
    bin_cols = pd.DataFrame(transformed, columns=titled_col_names)
    return bin_cols


def min_max_scale_df(df):
    """
    scale a dataframe to the smallest element is 0, and largest 1.
    :param df: the dataframe to min_max_scale
    :type df: pandas DataFrame
    """
    scaled = MinMaxScaler(feature_range=(0, 1), copy=True).fit_transform(df)
    scaled_df = pd.DataFrame(scaled, columns=df.columns)
    return scaled_df


imp_fun = {
    'female': impute_iden,
    'eventual186': impute_iden,
    'eventualnot186': impute_iden,
    'eventualnot186_with2nd': impute_iden,
    'map_testritscore': impute_mean,
    'map_testpercentile': impute_mean,
    'map_testdurationminutes': impute_mean,
    'map_percentcorrect': impute_mean,
    'map_start_date': impute_mean,
    'map_start_hour': impute_mean,
    'map_season': cat_binarizer,
    'map_reading_testritscore': impute_mean,
    'map_reading_testpercentile': impute_mean,
    'map_reading_testdurationminutes': impute_mean,
    'map_reading_percentcorrect': impute_mean,
    'map_reading_start_date': impute_mean,
    'map_reading_start_hour': impute_mean,
    'map_season': cat_binarizer,
    'map_max_score': impute_mean,
    'tripod_challenge_min': impute_mean,
    'tripod_challenge_max': impute_mean,
    'tripod_challenge_mean': impute_mean,
    'tripod_challenge_std': impute_mean,
    'tripod_classroom_management_min': impute_mean,
    'tripod_classroom_management_max': impute_mean,
    'tripod_classroom_management_mean': impute_mean,
    'tripod_classroom_management_std': impute_mean,
    'tripod_captivate_min': impute_mean,
    'tripod_captivate_max': impute_mean,
    'tripod_captivate_mean': impute_mean,
    'tripod_captivate_std': impute_mean,
    'tripod_care_min': impute_mean,
    'tripod_care_max': impute_mean,
    'tripod_care_mean': impute_mean,
    'tripod_care_std': impute_mean,
    'tripod_clarify_min': impute_mean,
    'tripod_clarify_max': impute_mean,
    'tripod_clarify_mean': impute_mean,
    'tripod_clarify_std': impute_mean,
    'tripod_consolidate_min': impute_mean,
    'tripod_consolidate_max': impute_mean,
    'tripod_consolidate_mean': impute_mean,
    'tripod_consolidate_std': impute_mean,
    'tripod_confer_min': impute_mean,
    'tripod_confer_max': impute_mean,
    'tripod_confer_mean': impute_mean,
    'tripod_confer_std': impute_mean,
    'tripod_cs_min': impute_mean,
    'tripod_cs_max': impute_mean,
    'tripod_cs_mean': impute_mean,
    'tripod_cs_std': impute_mean,
    'course_taken_art': impute_zeros,
    'course_taken_pe': impute_zeros,
    'course_taken_read': impute_zeros,
    'course_taken_science': impute_zeros,
    'course_taken_math': impute_zeros,
    'course_taken_social': impute_zeros,
    'course_taken_computer': impute_zeros,
    'course_taken_non_grade': impute_zeros,
    'course_taken_language': impute_zeros,
    'grade_mark_a': impute_zeros,
    'grade_mark_b': impute_zeros,
    'grade_mark_c': impute_zeros,
    'grade_mark_d': impute_zeros,
    'grade_mark_f': impute_zeros,
    'grade_mark_s': impute_zeros,
    'grade_mark_n': impute_zeros,
    'grade_mark_u': impute_zeros,
    'grade_mark_e': impute_zeros,
    'grade_mark_p': impute_zeros,
    'grade_mark_ng': impute_zeros,
    'rsa_log_rsa_retained': impute_zeros,
    'rsa_log_passed_itbs': impute_zeros,
    'rsa_log_probation_promoted': impute_zeros,
    'rsa_log_passed_occt': impute_zeros,
    'rsa_log_exemption': impute_zeros,
    'rsa_log_meets_rsa_criteria': impute_zeros,
    'iread_is_enrolled': impute_zeros,
    'iread_data_missing': impute_zeros,
    'iread_took_screener': impute_zeros,
    'iread_average_time_per_topic': impute_mean,
    'iread_average_sessions_per_week': impute_mean,
    'iread_current_series': impute_mean,
    'iread_current_topic': impute_mean,
    'iread_screener_placement_series': impute_mean,
    'iread_highest_unit_reached': impute_mean,
    'iread_total_sessions': impute_mean,
    'iread_total_topics_completed': impute_mean,
    'iread_total_time': impute_mean,
    'ethnicity': cat_binarizer,
    'age': impute_iden,
    'ell': cat_binarizer,
    'ell_language': cat_binarizer,
    'disability_code': cat_binarizer,
    'service_delivery': cat_binarizer,
    'lunch_status': cat_binarizer,
    'homeless': cat_binarizer,
    'lives_with': cat_binarizer,
    'school': cat_binarizer,
    'reenroll_num': impute_zeros,
    'reenroll_off_peak': impute_zeros,
    'reenroll_pss': impute_zeros,
    'reenroll_pns': impute_zeros,
    'reenroll_other': impute_zeros,
    'discipline_num': impute_zeros,
    'discipline_disobeyed_rules': impute_zeros,
    'discipline_disrespectful_behavior': impute_zeros,
    'discipline_harassment_bullying': impute_zeros,
    'discipline_no_information': impute_zeros,
    'discipline_skipping_class': impute_zeros,
    'discipline_repeated_behavior': impute_zeros,
    'discipline_disorderly_conduct': impute_zeros,
    'discipline_sexual_misconduct': impute_zeros,
    'discipline_possess_weapon': impute_zeros,
    'discipline_stealing': impute_zeros,
    'discipline_disruptive_conduct': impute_zeros,
    'discipline_physical': impute_zeros,
    'discipline_vandalism': impute_zeros,
    'rsa_summer_enrolled': impute_zeros,
    'rsa_summer_school': impute_zeros,
    'att_absence': impute_zeros,
    'att_tardiness': impute_zeros,
    'att_with_explanation': impute_zeros,
    'att_other': impute_zeros,
    'att_excused_absence': impute_zeros,
    'att_unexcused_absence': impute_zeros,
    'att_leave_early': impute_zeros,
    'att_school_activity': impute_zeros,
    'att_nurse': impute_zeros,
    'att_half_day_absence': impute_zeros,
    'att_in_school_suspension': impute_zeros,
    'att_truancy': impute_zeros,
    'att_counselor': impute_zeros,
    'att_administrator': impute_zeros,
    'tfa_summer_enrolled': impute_zeros,
    'tfa_summer_days_enrolled': impute_zeros,
    'tfa_teacher': cat_binarizer,
    'map_diff': impute_zeros,
    'map_total_diff': impute_zeros,
    'map_year_diff': impute_zeros,
    'map_std': impute_zeros,
    'map_num_tests': impute_zeros,
    'map_num_tests_term': impute_zeros,
    'map_num_consecutive_negs': impute_zeros
}


def make_imputed_col(colname, col, stuterm_df, scale):
    """
    Looks up colname in a the imp_fun dict and applys
    imputation on col, passing stuterm_df in case needed
    :param colname: the columns name
    :type colname: str
    :param col: the column data
    :type col: pandas.Series
    :param stuterm_df: the index of the column
    :type stuterm_df: pandas.DataFrame
    :param scale: which normalization function to use. Or none.
    :type scale: str like "l1", "l2", or None
    :returns: pandas.Dataframe of varying column width
    """
    imputed = imp_fun[colname](col, stuterm_df)
    imputed_df = pd.DataFrame(imputed)  # make sure return type is dataframe
    if not scale:  # i.e norm type is false
        return imputed_df
    else:
        scaled_df = min_max_scale_df(imputed_df)
        return scaled_df
