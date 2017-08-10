"""
Tulsa Schools Project

Upload all raw data into postgres database
Tulsa team, DSSG 2016
"""

import json
import sys
from optparse import OptionParser
from os import listdir
from os.path import abspath, basename, isfile, join
import pandas as pd

from tulsa.config import create_engine_from_config_file
from tulsa.etl.sql_str_normer import normalize_name_generic


def read_file_to_df(filename):
    """
    Take tablenames and a filename, read format from file extension (csv, tsv, or xsl(x))
    and return a dictionary of dataframes, keyed by table name.

    :param str filename: the filename to read
    :returns: dictionary of table_names and their DataFrames
    :rtype: dict[str,pandas.DataFrame]
    """
    basefile = basename(filename)
    global file_table_names
    table_name = file_table_names[basefile]
    filename_parts = basefile.split('.')
    filename_extension = filename_parts[-1]

    read_methods = {'csv': lambda x: pd.read_csv(x, engine='python'),
                    'tsv': lambda x: pd.read_csv(x, sep='\t'),
                    'xls': lambda x: pd.read_excel(x, sheetname=None),
                    'xlsx': lambda x: pd.read_excel(x, sheetname=None)}
    read_result = read_methods[filename_extension](filename)
    if filename_extension in ('csv', 'tsv'):
        # rename columns to not have symbols
        read_result.rename(columns=lambda x: normalize_name_generic(
            str(x), remove_leading_nums=False), inplace=True)
        df_dict = {table_name: read_result}
    elif filename_extension in ('xls', 'xlsx'):
        df_dict = {}
        for sheet_name, df in read_result.items():
            # rename columns to not have symbols
            df.rename(columns=lambda x: normalize_name_generic(
                str(x), remove_leading_nums=False), inplace=True)
            df_dict['{tablename}_{sheetname}'.format(
                tablename=table_name,
                sheetname=normalize_name_generic(
                    sheet_name, remove_leading_nums=False))] = df
    else:
        raise ValueError("Unsupported extension: {ext}".format(
            ext=filename_extension))
    return df_dict


def upload_df_to_db(engine, df_dict, schema='raw_data'):
    """
    Take an engine and dataframe to upload dataframe to engine.
    Use chunking strategy to prevent memory issues.

    :params sqlalchemy Engine engine: sql engine to upload to
    :params dict df_dict: dict of dataframes to upload
    returns: None
    rtype: None
    """
    for table_name, df in df_dict.items():
        df_shape = df.shape
        chunksize = df_shape[0] // 10 + 1
        df.to_sql(table_name, engine, index=False, schema=schema,
                  if_exists='replace', chunksize=chunksize)
        print('success', table_name)


def main():
    """
    Use user-inputted command-line arguments through argparse library
    to upload text files to a database table
    """
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename_to_upload',
                      help='just upload this one file')
    parser.add_option('-d', '--dir', dest='dir_to_upload',
                      help='upload everything in this dir')
    parser.add_option('-c', '--config', dest='config_file',
                      help='where to get database credential file')
    parser.add_option('-n', '--names', dest='file_table_names_file_path',
                      help='where the file_table_names json file is stored')

    (options, args) = parser.parse_args()

    filenames_to_upload = []
    if options.filename_to_upload:
        absfile = abspath(options.filename_to_upload)
        filenames_to_upload.append(absfile)

    elif options.dir_to_upload:
        for f in listdir(options.dir_to_upload):
            absfile = join(options.dir_to_upload, f)
            if isfile(absfile):
                filenames_to_upload.append(absfile)
    else:
        print('no files specified to upload...quitting')
        sys.exit(0)

    # create engine to connect to postgres
    print(options.config_file)
    engine = create_engine_from_config_file(options.config_file)

    with open(options.file_table_names_file_path, 'r') as f:
        global file_table_names
        file_table_names = json.load(f)

    for filename in filenames_to_upload:
        df_dict = read_file_to_df(filename)
        upload_df_to_db(engine, df_dict)


if __name__ == '__main__':
    main()
