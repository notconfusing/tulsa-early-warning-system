"""
Create clean iRead tables and view
"""
import pandas as pd

from tulsa.config import create_engine_from_config_file

config_file = '/path/to/configs/dbcreds.json'
engine = create_engine_from_config_file(config_file)

get_table_info_query = """
                       SELECT *
                       FROM pg_catalog.pg_tables
                       WHERE schemaname = 'raw_data'
                           AND tablename ~ 'iread.*';
                       """
tables = engine.execute(get_table_info_query)
tables = tables.fetchall()
table_names = [table['tablename'] for table in tables]

# look at column names
def column_names(table):
    # note: .keys() gets the column names
    return engine.execute('''SELECT * FROM raw_data."{table}"'''.format(table=table)).keys()

# create a dictionary with column names for each table
columns_dict_old = {tablename: column_names(tablename) for tablename in table_names}

# turn into a df for easy viewing
col_name_df = pd.DataFrame.from_dict(columns_dict_old, orient="index")
col_name_df.fillna(value='', inplace=True)

# only keep iread-related SID and grade for now
# ALSO : S44JR_ENROLLED: enrolled in iRead
# anything starting with 'iread'

# get set unique column names for iread in order to join all the years
def iread_col_names(col):
    return [x for x in col_name_df.T.iloc[:, col] if 'IREAD' in x]
ireads = [iread_col_names(x) for x in range(0, 5)]
result = set(ireads[0])
for s in ireads[1:]:
    result.intersection_update(s)
# the first year doesn't have the daterange variables, but want to keep those,
# so add them in to the set
ireads_to_keep = list(result) + [x for x in col_name_df.T.iloc[:,4] if 'IREAD_DATERANGE' in x ]

cols_to_keep_for_view = ['SIS_ID', 'GRADE', 'EXPORT_START_DATE', 'EXPORT_END_DATE', 'S44JR_ENROLLED'] + ireads_to_keep

# clean col names function
def clean_column_name(x):
    out = x.lower()
    out = out.strip()
    return out

# The iread tables that were provided for each year are in different formats
# so do each year separately
# 2013-14
# need to add in the daterange columns, which don't exist
# select statement
ctk_14 = [x for x in cols_to_keep_for_view if 'IREAD_DATERANGE' not in x]
daterange_cols = [clean_column_name(x) for x in cols_to_keep_for_view if 'IREAD_DATERANGE' in x]
col_dict = dict(zip(ctk_14, [clean_column_name(x) for x in ctk_14]))
daterange_types = ['text', 'float', 'int', 'int', 'float']
daterange_dict = dict(zip(daterange_cols, daterange_types))
as_statement = ','.join(['\"' + key + '\"' + ' AS ' + value for key, value in col_dict.items()]) +','+ ','.join(['CAST(NULL AS '+y+') AS ' +x for x,y in daterange_dict.items()])

query = 'CREATE TABLE clean_data.iread_13_14 AS SELECT ' + as_statement + ' FROM raw_data.iread_14'
engine.execute(query)

# 2014-15: SPECIAL CASE
# there are two tables with slightly different groups of students
# join then remove the duplicates
d = pd.read_sql_query('SELECT * FROM raw_data.iread_15_reduced_columns', engine)
d2 = pd.read_sql_query('SELECT * FROM raw_data.iread_15_full_columns', engine)
df = d[cols_to_keep_for_view]
df = df.append(d2[cols_to_keep_for_view])
iread_15 = df.loc[df.duplicated('SIS_ID') == False]
iread_15.columns = [clean_column_name(x) for x in iread_15.columns]
iread_15.to_sql('iread_14_15', engine, schema='clean_data', index=False)

# 2015-16
# Like 2013-14 but no missing cols
# use full year only
# change daterange_current_series_topic to text
col_dict = dict(zip(cols_to_keep_for_view, [clean_column_name(x) for x in cols_to_keep_for_view]))
# change daterange_current_series_topic to text
del col_dict['IREAD_DATERANGE_CURRENT_SERIES_TOPIC']
as_statement = ','.join(['\"' + key + '\"' + ' AS ' + value for key, value in col_dict.items()]) + ', CAST("IREAD_DATERANGE_CURRENT_SERIES_TOPIC" as text) as iread_daterange_current_series_topic'

query = 'CREATE TABLE clean_data.iread_15_16 AS SELECT ' + as_statement + ' FROM raw_data.iread_16_full_year'
engine.execute(query)

# Create iread view
# Need to order columns before joining
cols_order = ','.join(['\"' + clean_column_name(x) + '\"' for x in cols_to_keep_for_view])
query = '''
        CREATE VIEW clean_data.iread AS
        SELECT {cols_order}, '13_14' AS measured_year
        FROM clean_data.iread_13_14
        UNION SELECT {cols_order}, '14_15' AS measured_year
        FROM clean_data.iread_14_15
        UNION SELECT {cols_order}, '15_16' AS measured_year FROM clean_data.iread_15_16
        '''.format(cols_order=cols_order)
query
engine.execute(query)
