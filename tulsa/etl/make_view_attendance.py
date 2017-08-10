"""
Make view of attendance data from clean attendance tables
"""

import re

from tulsa.config import create_engine_from_config_file

config_file = '/path/to/configs/dbcreds.json'
engine = create_engine_from_config_file(config_file)
# get all clean tables that have attendance data
get_table_info_query = """
                       SELECT *
                       FROM pg_catalog.pg_tables
                       WHERE schemaname = 'clean_data'
                           AND tablename ~ 'attendance.*';
                       """
att_tables = engine.execute(get_table_info_query)
att_tables = att_tables.fetchall()
att_table_names = [table['tablename'] for table in att_tables]

# create some year variables
years = [re.findall('[0-9][0-9]\_[0-9][0-9]', table_name)[0] for table_name in att_table_names]
years_num = [re.findall('[0-9][0-9]\_', table_name)[0] for table_name in att_table_names]
years_num = [int('20' + re.sub("\_", "", year)) for year in years_num]
tablename_year_dict = dict((z[0], list(z[1:])) for z in zip(att_table_names,years,years_num))
tablename_year_dict.items()


def create_select_statement(tablename, year, year_num):
    select_statement = """
                       SELECT *, '{year}' AS measured_year, {year_num} AS start_year
                       FROM clean_data.{tablename}
                       """.format(tablename=tablename, year=year, year_num=year_num)
    return select_statement


def create_view_statement(tablename_dict):
    select_statements_list = [create_select_statement(tablename, year, year_num) 
                              for tablename, [year, year_num] in tablename_dict.items()]
    select_statements = ' UNION '.join(select_statements_list)
    view_statement = """CREATE VIEW clean_data.attendance AS
                         {select_statements};
                     """.format(select_statements=select_statements)
    return view_statement

view_statement = create_view_statement(tablename_year_dict)
engine.execute(view_statement)
