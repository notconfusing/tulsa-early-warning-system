"""
Clean reenrollment asssessment table from raw
"""
from optparse import OptionParser
from tulsa.config import create_engine_from_config_file
from tulsa.etl.sql_str_normer import normalize_colname, normalize_tablename
from collections import Counter
import sys
import json


def load_intorbust(engine):
    '''
    load the intorbust sql function into the connection.
    intorbust makes all the values of a column an int or null if not possible.

    :param engine: the engine to load intorbust into
    :type engine: sqlalchemy engine
    :param sqlfile: the filename/location of the intorbust code
    :type sqlfile: str
    '''

    sql_str = r'''create or replace function isdigits(text) returns boolean
       as 'select $1 ~ ''^(-)?[0-9]+$'' as result'
       language sql
       immutable
       RETURNS NULL ON NULL INPUT;

    create or replace function intorbust(text) returns int
    as 'select
       	  case isdigits($1) when TRUE then cast($1 as int)
	  else null
	  end'
       language sql
       immutable
       RETURNS NULL ON NULL INPUT;

    create or replace function intorbust(numeric) returns numeric
       as 'select $1'
       language sql
       immutable
       RETURNS NULL ON NULL INPUT;

    create or replace function intorbust(float) returns float
       as 'select $1'
       language sql
       immutable
       RETURNS NULL ON NULL INPUT;
    '''
    engine.execute(sql_str)


def get_tables_with_prefix(engine, prefix, schemaname):
    '''
    return a list of the table names that begin with prefix in a specific
    schema

    :param engine: the engine to use
    :type engine: sqlalchemy engine
    :param prefix: the prefix to use in selecting tables
    :type prefix: str
    :param schemaname: schemaname to search with
    :type schemaname: str

    :returns: list[str] -- the table names beginning with prefix of schema
    '''
    get_tables_query = """select tablename
                              from pg_catalog.pg_tables
                              where schemaname = '{schemaname}'
                              and tablename ~ '{prefix}.?';
                              """.format(prefix=prefix, schemaname=schemaname)
    query_tables = engine.execute(get_tables_query).fetchall()
    query_tables_strs = [q['tablename'] for q in query_tables]
    return query_tables_strs


def column_names(engine, table, schemaname):
    '''
    return the columns names of a table and a schema

    :param engine: the engine to use
    :type engine: sqlalchemy engine
    :param table: the table name in question
    :type table: str
    :param schemaname: the schema name from which the table exists
    :type schemaname: str
    :returns: list[str] -- the column names of the table
    '''
    return engine.execute('''SELECT * FROM {schemaname}."{table}"
                          '''.format(table=table,
                                     schemaname=schemaname)).keys()


def drop_table(engine, table, schemaname):
    '''
    drop table from schema, cascading if necessary

    :param engine: the engine to use
    :type engine: sqlalchemy engine
    :param table: the table name to drop
    :type table: str
    :param schemaname: the schema name from which the table exists
    :type schemaname: str
    '''
    dropsql = '''DROP TABLE IF EXISTS {}.{} CASCADE;
              '''.format(schemaname, table)
    engine.execute(dropsql)


def clean_data_create_select_column_from_old(
        old_colnames_list, columns_in_all_tables, corrections):
    '''
    Creates select column subclauses with AS statments to clean names,
    returns "as" string of select colnames as new.

    :param old_colnames_list: the colnames from raw that need to be cleaned
    :type old_colnames_list: list[str]
    :param columns_in_all_tables: the column names that are common
                                                after normalization
    :type columns_in_all tables: set
    :returns str: a string of "as" statements
     '''
    new_colnames_list = [normalize_colname(name, corrections=corrections)
                         for name in old_colnames_list]
    old_new_colnames = list(zip(old_colnames_list, new_colnames_list))
    intersection_old_new_colnames = [(old, new) for
                                     old, new in old_new_colnames
                                     if new in columns_in_all_tables]
    as_statements = []
    for old, new in intersection_old_new_colnames:
            if new in ['studentid']:
                as_statement = 'intorbust("{old}") AS {new}'.format(old=old,
                                                                    new=new)
                as_statements.append(as_statement)
            else:
                as_statement = '"{old}" AS {new}'.format(old=old, new=new)
                as_statements.append(as_statement)

    as_string = ', '.join(as_statements)
    return as_string


def clean_data_create_select_statement(tablename, old_colnames_list,
                                       columns_in_all_tables, corrections):
    '''
    Creates select statements given AS statments

    :param tablename: the table name from which were selecting
    :type tablename: str
    :param old_colnames_list: the colnames from raw that need to be cleaned
    :type old_colnames_list: list[str]
    :param columns_in_all_tables: the column names that are
                                        common after normalization
    :type columns_in_all tables: set
    :returns str: select statement
    '''
    as_statements = clean_data_create_select_column_from_old(
        old_colnames_list, columns_in_all_tables, corrections)
    select_statement = """SELECT {as_statements}
                        FROM raw_data."{tablename}"
                        """.format(as_statements=as_statements,
                                   tablename=tablename)
    return select_statement


def clean_data_create_copy_statement(raw_tablename, old_colnames_list,
                                     columns_in_all_tables, corrections):
    '''
    makes a CREATE TABLE statement given a raw_tablename and does casting to
    numeric where possible

    :param raw_tablename: the table name from which were selecting
    :type str:
    :param old_colnames_list: the colnames from raw that need to be cleaned
    :type old_colnames_list: list[str]
    :param columns_in_all_tables: the column names that are common
                                                after normalization
    :type columns_in_all tables: set
    :returns str: sql create table statement
    '''
    select_statement = clean_data_create_select_statement(
        raw_tablename, old_colnames_list, columns_in_all_tables, corrections)
    clean_table_name = normalize_tablename(raw_tablename)
    copy_statement = """CREATE TABLE clean_data.{tablename} AS
                        {select_statement};
                    """.format(tablename=clean_table_name,
                               select_statement=select_statement)

    return copy_statement


def create_select_statement(tablename, colnames_list, time_from_title):
    """
    create select statement from column name
    additionally making dates form titles if specificed
    format should be _{YY}_{season} where YY is a year
    and season is one of 'fall', 'winter', or 'spring'

    :param tablename: the table name to select from
    :type tablename: str
    :param colnames_list: the colnames to select
    :type colnames: list[str]
    :param time_from_title: whether to try and get date information from title
    :type time_from_tile: bool
    :returns str: sql select statements
    """
    extra_time_cols = ''
    if time_from_title:
        tablename_parts = tablename.split('_')
        cal_year = tablename_parts[1]
        season = tablename_parts[-1]
        if season == 'fall':
            measured_year = cal_year + '_' + str(int(cal_year) + 1)
        elif season in ['winter', 'spring']:
            measured_year = str(int(cal_year) - 1) + '_' + cal_year
        extra_time_cols = """, '{measured_year}'::varchar as measured_year,
                            '{season}'::varchar as season,
                            '{cal_year}'::int as cal_year
                          """.format(measured_year=measured_year,
                                     season=season,
                                     cal_year=cal_year)
    all_columns = ', '.join(colnames_list)
    select_statement = """SELECT {all_columns} {extra_time_cols}
                        FROM clean_data.{tablename}
                        """.format(tablename=tablename,
                                   extra_time_cols=extra_time_cols,
                                   all_columns=all_columns)
    return select_statement


def create_view_statement(columns_dict, view_name, time_from_title):
    """
    create view statement from all the tables and columns in columns dict
    additionally making dates form titles if specificed

    :param columns_dict: a mapping between table names and their column names
    :type columns_dict: dict[str: list]
    :param view_name: what to name the view
    :type view_name: str
    :param time_from_title: whether to try and get date information from title
    :type time_from_tile: bool
    :returns str: sql create view statement
    """

    select_statements_list = [create_select_statement(tablename,
                                                      old_colnames_list,
                                                      time_from_title)
                              for tablename, old_colnames_list
                              in columns_dict.items()]
    select_statements = ''' UNION
                        '''.join(select_statements_list)
    view_statement = """CREATE OR REPLACE VIEW clean_data.{view_name} AS
                        {select_statements};
                    """.format(select_statements=select_statements,
                               view_name=view_name)
    return view_statement


def main(engine, options):
    load_intorbust(engine)

    # find the raw tables to operate over
    raw_tables = []
    if options.raw_table:
        raw_tables.append(options.raw_table)
    elif options.raw_table_prefix:
        prefix_table_names = get_tables_with_prefix(engine,
                                                    options.raw_table_prefix,
                                                    'raw_data')
        raw_tables.extend(prefix_table_names)
    else:
        print('no tables specified... use --prefix or --table')
        sys.exit(1)
    print('going to operate on these raw tables: {}'.format(raw_tables))

    # make a dictionary of raw_tables and their associated column names
    raw_dict = {raw_table: column_names(engine, raw_table, 'raw_data')
                for raw_table in raw_tables}

    if options.corrections:
        corrections = json.load(open(options.corrections, 'r'))
    else:
        corrections = None

    # find the common columns in all tables -- after column name normalization.
    column_count = Counter()
    for raw_table, raw_columns in raw_dict.items():
        normed_colnames = [normalize_colname(col, corrections=corrections)
                           for col in raw_columns]
        for normed_colname in normed_colnames:
            column_count[normed_colname] += 1

    columns_in_all_tables = [col for col, cnt in column_count.items()
                             if cnt == len(raw_tables)]

    # make the destination tables and drop them if necessary
    clean_tables = [normalize_tablename(raw_table) for raw_table in raw_tables]
    for clean_table in clean_tables:
        drop_table(engine, clean_table, 'clean_data')

    # perform the raw -> clean copy
    for raw_table, raw_columns in raw_dict.items():
        copy_statement = clean_data_create_copy_statement(
            raw_table,
            raw_columns,
            columns_in_all_tables,
            corrections=corrections)

        print(copy_statement)
        engine.execute(copy_statement)
    print("look for clean_data.{}".format(clean_tables))

    # now to make the view
    # make a dictionary of clean_tables and their associated column names
    clean_dict = {clean_table: column_names(engine, clean_table, 'clean_data')
                  for clean_table in clean_tables}

    view_statement = create_view_statement(clean_dict,
                                           options.view_name,
                                           options.time_from_title)
    engine.execute(view_statement)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-t', '--table', dest='raw_table',
                      help='specify 1 raw table name')
    parser.add_option('-p', '--table_prefix', dest='raw_table_prefix',
                      help='specificy a prefix of all raw table names')
    parser.add_option('-c', '--config', dest='config_file',
                      help='where to get database credential file')
    parser.add_option('-v', '--view_name', dest='view_name',
                      help='what the final view name should be')
    parser.add_option('-e', '--date_cols_from_title',
                      action="store_true",
                      dest='time_from_title',
                      help='''turn this flag on if you want date/season columns
                              extracted from the table names''')
    parser.add_option('-o', '--corrections',
                      dest='corrections',
                      help='''point to a json dict of column names you want to
                              change''')

    (options, args) = parser.parse_args()

    engine = create_engine_from_config_file(options.config_file)

    if not options.config_file:
        print('no database credentials json file specified use --config /path')
        sys.exit(1)
    if not options.view_name:
        print('no destination view name specified use --view_name name')
        sys.exit(1)
    else:
        main(engine, options)
