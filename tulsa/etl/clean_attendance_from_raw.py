"""
Clean annual attendance data from raw tables

Note: This is not used as a feature in the model, due to eventual
available daily attendance data
"""

import pandas as pd

from tulsa.config import create_engine_from_config_file

config_file = '/path/to/configs/dbcreds.json'
engine = create_engine_from_config_file(config_file)

# get all tables that are have attendance data
get_table_info_query = """
                       SELECT *
                       FROM pg_catalog.pg_tables
                       WHERE schemaname = 'raw_data'
                           AND tablename ~ '^attendance.*'
                           AND not tablename ~ '.*full';
                       """
att_tables = engine.execute(get_table_info_query)
att_tables = att_tables.fetchall()
att_table_names = [table['tablename'] for table in att_tables]
# define new table names
att_tables_new_names = [x.replace('_sheet1', '') for x in att_table_names]
# dictionary of old and new table names
att_tables_old_new_dict = dict(zip(att_table_names, att_tables_new_names))
att_tables_old_new_dict


def column_names(table):
    # note: .keys() gets the column names
    return engine.execute('''SELECT * FROM raw_data."{table}"'''.format(table=table)).keys()

# create a dictionary with column names for each table
att_columns_dict_old = {tablename: column_names(tablename) for tablename in att_table_names}

# turn into a df for easy viewing
col_name_df = pd.DataFrame.from_dict(att_columns_dict_old, orient="index")
col_name_df.fillna(value='', inplace=True)

# create some clean column names
def clean_column_name(x):
    out = x.lower()
    out = out.strip()
    r = out.replace(' ', '_')
    return r

clean_col_name_df = col_name_df.applymap(clean_column_name)
clean_col_names = list(clean_col_name_df.iloc[2, :])

# define column variable types
types = ['text', 'int', 'float', 'float', 'float', 'int']
col_type_dict = dict(zip(clean_col_names, types))


def create_as_statement(old_name, col_type, new_name):
    if(col_type == 'text'):
        as_statement = '''CAST("{old_name}" AS {col_type}) AS {new_name}'''.format(old_name=old_name, col_type=col_type, new_name=new_name)
    else:
        as_statement = '''CASE WHEN isnumeric(CAST ("{old_name}" AS text)) THEN CAST("{old_name}" AS {col_type}) ELSE NULL END {new_name}'''.format(old_name=old_name, col_type=col_type, new_name=new_name)
    return(as_statement)

# function to check if cell is number
engine.execute('''
CREATE OR REPLACE FUNCTION isnumeric(text) RETURNS BOOLEAN AS $$
DECLARE x NUMERIC;
BEGIN
    x = $1::NUMERIC;
    RETURN TRUE;
EXCEPTION WHEN others THEN
    RETURN FALSE;
END;
$$
STRICT
LANGUAGE plpgsql IMMUTABLE;
''')


# need to create 'full' clean tables for all years
# full means include "off_roll" as NULL column for all years except 15-16
def create_full_clean_table(old_table, new_table):
    if(len(att_columns_dict_old[old_table]) == 5):
        as_statement_temp = ', '.join([create_as_statement(att_columns_dict_old[old_table][x], 
                                       types[x], clean_col_names[x]) for x in range(0, len(clean_col_names)-1)])
        as_statement = as_statement_temp + ', CAST(NULL AS int) AS off_roll'
    else:
        as_statement = ', '.join([create_as_statement(att_columns_dict_old[old_table][x],
                                                      types[x], clean_col_names[x]) for x in range(0, len(clean_col_names))])
    create_att_table_full_columns = '''
                                    CREATE TABLE clean_data."{new_table}" AS 
                                    SELECT {as_statement}
                                    FROM raw_data."{old_table}";
                                    '''.format(new_table=new_table, old_table=old_table, as_statement=as_statement)

    engine.execute(create_att_table_full_columns)
    delete_null_ids = '''
                    DELETE FROM clean_data."{new_table}" WHERE student_number is null OR char_length(student_name)<3;
                    '''.format(new_table=new_table)
    engine.execute(delete_null_ids)

# loop over tables and clean
for old_table, new_table in att_tables_old_new_dict.items():
    print(old_table, new_table)
    create_full_clean_table(old_table, new_table)
