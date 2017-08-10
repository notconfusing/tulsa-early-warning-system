from tulsa.learn import evaluate
from tulsa.learn import features
from tulsa.learn import prepare
from tulsa.learn import splits
from tulsa.learn import helpers
from tulsa.learn import report

import logging
import pandas as pd
import numpy as np
import time
from datetime import datetime

class TulsaModel(object):
    """ A class containing prodecures to build, train, and evaluate a
    machine learning model.

    :param engine: sqlalchemy engine to get database information
    :param features_to_make: the features to make
    :param label_name: which labels are we using
    :param model_name: machine learning model to use
    :param split_strategy: the strategy to create test/train splits
    :param regenerate: flag if labels should be regenerated rather than read 
                       from db
    :type engine: sqlalchemy engine
    :type features_to_make: list[str]
    :type label_name: str
    :type model_name: str
    :type split_strategy: str
    :type regenerate: bool
    """
    def __init__(self, engine,
                 features_to_make,
                 label_name,
                 models_to_make,
                 metrics_to_make,
                 splits_to_make,
                 regenerate,
                 run_name,
                 state_location,
                 scale):
        self.features_to_make = features_to_make
        self.engine = engine
        self.label_name = label_name
        self.models_to_make = models_to_make
        self.metrics_to_make = metrics_to_make
        self.splits_to_make = splits_to_make
        self.regenerate = regenerate
        self.run_name = run_name
        self.state_location = state_location
        self.run_number = helpers.get_next_ver_number(self.run_name,
                                                      self.state_location)
        self.scale = scale
        self.label_feature_df = None
        logging.debug('regeneration is: %s', self.regenerate)
        logging.debug('scaling is : %s', self.scale)

    def make_labels(self):
        """Creates labels based on label_name
        stores the associated labels and index as class attributes
        """
        self.stuterm_df, self.labels = features.make_feature_from_str(
            self.label_name,
            self.engine,
            stuterm_df=None)

        self.labels.name = self.label_name
        self.label_feature_df = self.labels

    def load_cols(self, cols):
        """Load columns cols from feature databas
        :param cols: the columns to laod
        :type cols: list[str]
        :returns: pandas DataFrame of columns
        """
        cols_str = ', '.join(cols)
        load_feats_sql = """SELECT {cols_str}
                         FROM features.{label_name}
                         ;""".format(cols_str=cols_str,
                                     label_name=self.label_name)
        return pd.read_sql(load_feats_sql, self.engine)

    def load_labels(self):
        """Try to loads labels from the database
        """
        self.labels = self.load_cols([self.label_name])
        self.stuterm_df = self.load_cols(['studentid',
                                          'measured_year',
                                          'season'])
        self.label_feature_df = self.labels

    def generate_labels(self):
        """Find a method  to generate labels based on label_name
        stores the associated labels and index as class attributes
        """
        if self.regenerate:  # is the flag on
            self.make_labels()
        else:                # otherwise try and load first
            logging.debug('label_name is %s', self.label_name)
            features_in_db, features_not_in_db = self.feature_column_exists([self.label_name])
            if features_in_db:
                self.load_labels()
            else:
                self.make_labels()

    def make_features(self, features_to_create):
        """Creates features for everything in features_to_create.
        This stores the faetures in label_feature_df, so you don't have to load them as well.
        """
        for feature_name in features_to_create:
            logging.debug('trying to make feature %s', feature_name)
            unnamed_feat = features.make_feature_from_str(feature_name,
                                                          self.engine,
                                                          self.stuterm_df)
            feat = pd.DataFrame(unnamed_feat)  # make sure this is not a series
            feat.columns = [feature_name]
            self.label_feature_df = pd.concat([self.label_feature_df, feat], axis=1)

    def load_features(self, features_to_load):
        """Try to loads features from the database
        :param features_to_load: the features to load
        :type features_to_load: list[str]
        """
        loaded_features = self.load_cols(features_to_load)
        self.label_feature_df = pd.concat([self.label_feature_df, loaded_features], axis=1)

    def feature_column_exists(self, feature_name_list):
        """determine if a feature column exists
        in the feature table associated with the label name

        :param feature_name_list: the feature names
        :type feature_name: list[str]
        :returns: tuple ([features_in_db], [features_not_in_db])
        """
        get_columns_query = """SELECT column_name
                                FROM information_schema.columns
                                WHERE table_schema = 'features'
                                  AND table_name   = '{label_name}'
                                  """.format(label_name=self.label_name)
        fetched = self.engine.execute(get_columns_query).fetchall()
        column_names = [row[0] for row in fetched]
        logging.debug('Columns I found in features. %s are: %s',
                      self.label_name, column_names)
        features_in_db = []
        features_not_in_db = []
        for feat in feature_name_list:
            if feat in column_names:
                features_in_db.append(feat)
            else:
                features_not_in_db.append(feat)
        return (features_in_db, features_not_in_db)

    def generate_features(self):
        """create or load feates based on label_name
        """
        if self.regenerate:
            self.make_features(self.features_to_make)
            self.save_all_data_to_db()  # save it all
        else:
            features_in_db, features_not_in_db = self.feature_column_exists(self.features_to_make)

            logging.debug("Features to make: %s", self.features_to_make)
            logging.debug("Features found in DB: %s", features_in_db)
            logging.debug("Features not found in DB: %s", features_not_in_db)

            if features_in_db:  # load in what we can
                self.load_features(features_in_db)
            if features_not_in_db:   # make the rest
                self.make_features(features_not_in_db)
                self.add_columns_to_existing_db(features_not_in_db)
                # only save if there were things not in the db
        logging.info("Generated features: %s",
                     list(self.label_feature_df.columns))

    def add_columns_to_existing_db(self, features_not_in_db):
        """sort of append features onto existing database
        :param features_not_in_db: the features to add to the db now
        :type features_not_in_db: list[str]
        """
        not_in_df = self.label_feature_df[features_not_in_db]
        temp_data_df = pd.concat([self.stuterm_df, not_in_df], axis=1)
        temp_data_df.to_sql(name='temp',
                            con=self.engine,
                            schema='features',
                            if_exists='replace',
                            index=False)
        for feat in features_not_in_db:
            logging.debug('trying to add to features table', feat)
            helpers.alter_features_add_column('temp', feat, self.label_name, self.engine)

    def save_all_data_to_db(self):
        """put together all dataframes in the format
        [studentid, measured_year, season, label, features ...]
        ^                                  ^
        stuterm_df                         label_feature_df
        """
        logging.debug('trying to make all data df')
        all_data_df = pd.concat([self.stuterm_df, self.label_feature_df], axis=1)
        # this can take a while so timing it
        start_time = time.time()
        all_data_df.to_sql(name=self.label_name,
                           con=self.engine,
                           schema='features',
                           if_exists='replace',
                           index=False)
        end_time = time.time()
        time_taken = end_time - start_time
        logging.info('Saving Time: %s seconds', time_taken)
        logging.info('all data saved to features')
        logging.debug('saved %s rows', len(all_data_df))

    def make_splits(self):
        """
        Makes a list of (X_test, X_train, y_test, y_train) splits.
        """
        self.splits = {}
        for split_strategy in self.splits_to_make:
            curr_split = splits.make_splits(split_strategy,
                                            self.stuterm_df,
                                            self.label_feature_df,
                                            self.engine)
            self.splits[split_strategy] = curr_split
        for split_strategy, test_dict in self.splits.items():
            for test_name, split in test_dict.items():
                logging.info('split strategy is %s', split_strategy)
                logging.debug('____for %s ____', test_name)
                logging.debug('X_train is length %s', len(split['X_train']))
                logging.debug('X_test is length %s', len(split['X_test']))
                logging.debug('y_train is length %s', len(split['y_train']))
                logging.debug('y_test is length %s', len(split['y_test']))
                logging.debug('Train class prior is %s', np.mean(split['y_train']))
                logging.debug('Test class prior is %s', np.mean(split['y_test']))


    def fit_models_and_metrics(self):
        """Fit all models in models_to_make on the test parts of each
        split from self.splits and make all metrics.
        """
        # store the y_preds of the splits
        self.splits_y_preds = {}
        # store the feat_imps of the splits
        self.splits_feat_imps = {}

        for split_strategy, test_dict in self.splits.items():

            # were going to associate splits with y_preds and featimps
            self.splits_y_preds[split_strategy] = dict()
            self.splits_feat_imps[split_strategy] = dict()

            for test_name, split in test_dict.items():
                result_list, feat_imp_df, feat_crosstab, y_preds_df = \
                    evaluate.fit_models_and_metrics(split['X_train'],
                                                    split['X_test'],
                                                    split['y_train'],
                                                    split['y_test'],
                                                    self.models_to_make,
                                                    self.metrics_to_make)

                # TODO: could results be returned as DFs
                # so that they could be handle more easily
                for result in result_list:
                    result.extend([test_name,
                                   split_strategy,
                                   self.label_name,
                                   self.features_to_make])
                    self.write_results(result)
                    # final order: (model_name, params, metric_name, metric_value,
                    # test_name, split_strategy, label_name, features_to_make)

                # keep the y_preds together with the test_name
                assert len(split['test_stuterm']) == len(y_preds_df)
                stuterm_preds = pd.concat([split['test_stuterm'].reset_index(),
                                           y_preds_df],
                                          axis=1)
                self.splits_y_preds[split_strategy][test_name] = stuterm_preds
                self.splits_feat_imps[split_strategy][test_name] = feat_imp_df

                # we need love too
                tab_df = {'feat_imp': feat_imp_df,
                          'feat_crosstab': feat_crosstab,
                          'y_preds': stuterm_preds}

                for table_name, df in tab_df.items():
                    df['test_name'] = test_name
                    self.upload_result_to_db(df, table_name=table_name)

    def impute_missing_values(self):
        """Impute missing values on the label_feature dataframe
        using column specific strategies defined in prepare module.
        """
        cols_before = len(self.label_feature_df.columns)
        imputed_label_feature_df = pd.DataFrame()
        for col_name in self.label_feature_df.columns:
            logging.debug('trying to impute col %s', col_name)
            col = self.label_feature_df[col_name]
            scale = False if col_name == self.label_name else self.scale
            num_nans_before = col.isnull().sum()
            imputed_col = prepare.make_imputed_col(col_name,
                                                   col,
                                                   self.stuterm_df,
                                                   scale)
            num_nans_after = imputed_col.isnull().sum()
            if not scale:
                logging.debug('Im not scaling %s ', col_name)

            logging.debug('after scaling %s has mean %s',
                          col_name, imputed_col.mean())

            logging.debug("NaNs before imputation: %s, after: %s", num_nans_before,
                          num_nans_after)
            imputed_label_feature_df = pd.concat(
                (imputed_label_feature_df, imputed_col), axis=1)

            imputed_col_names = list(imputed_col.columns)

            if len(imputed_col_names) > 1:
                # imputed_col may be a dataframe exploded from categorical
                # so we cannot simply replace the old col_name
                logging.debug("Exploded %s into %s", col_name, imputed_col_names)

        cols_after = len(imputed_label_feature_df.columns)
        logging.info('Columns before cat binarizing %s, columns after %s',
                     cols_before, cols_after)

        self.label_feature_df = imputed_label_feature_df

    def warn_nans(self):
        """Warn when NaNs are being dropped
        """
        non_nan_indexes = list(self.label_feature_df[self.label_feature_df.notnull().all(axis=1)].index)
        non_nan_label_feature = self.label_feature_df.dropna(axis=0, how='any')
        non_nan_stuterm = self.stuterm_df.iloc[non_nan_indexes]
        num_nan_rows = len(self.label_feature_df) - len(non_nan_label_feature)
        logging.warn('I found %s rows with a NaN', num_nan_rows)
        logging.warn('Just for YOU, I will drop NaN rows to continue, but get your shit together')
        self.label_feature_df = non_nan_label_feature
        self.stuterm_df = non_nan_stuterm

    def write_results(self, result_row):
        """Write metric results to database
        :param results_row: the results of a ml run
        :type results_row: list[list[object]]
        """
        results_col = ('model_name', 'params', 'metric_name', 'metric_value',
                       'run_time', 'test_name', 'split_strategy', 'label_name',
                       'features_to_make')
        results_table = pd.DataFrame.from_records([result_row],
                                                  columns=results_col)
        results_table['params'] = results_table['params'].apply(lambda x: str(x))
        self.upload_result_to_db(results_table, table_name='results')

    def upload_result_to_db(self, results_table, table_name):
        """
        write a result table to database
        :param result_table: the table to upload
        :param table_name: the table name in the 'results' schema
        :type result_table: pandas DataFrame
        :type table_name: str
        """
        results_table['time'] = str(datetime.now())
        results_table['run_name'] = '{}_{}'.format(self.run_name, self.run_number)
        results_table.to_sql(name=table_name, schema='results',
                             con=self.engine, if_exists='append', index=False)

    def touch_run_number(self):
        """Enumerate run number
        """
        helpers.touch_run_number(self.run_name, self.run_number, self.state_location)

    def report_predictions(self, report_name):
        logging.info('Reporting type is: %s', report_name)
        # have to make student-latest school relation first
        self.stu_school_df = report.make_stu_school_df(self.engine)
        # now for every split
        for split_strategy, test_dict in self.splits.items():
            for test_name, split in test_dict.items():
                y_preds = self.splits_y_preds[split_strategy][test_name]
                feat_imp_df = self.splits_feat_imps[split_strategy][test_name]
                if report_name == 'with_recs':
                    logging.debug('report name was with_recs, so making stu_most_improv')
                    stu_most_improv = report.make_stu_feat_df(self.label_feature_df,
                                                              self.stuterm_df,
                                                              feat_imp_df)
                    logging.debug('len of stu_most_improv is %s, ', len(stu_most_improv))
                else:
                    stu_most_improv = None
                report.write_report(self.stu_school_df,
                                    stu_most_improv,
                                    y_preds,
                                    test_name)
