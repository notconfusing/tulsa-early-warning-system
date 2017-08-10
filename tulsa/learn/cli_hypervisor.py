from tulsa.learn import model
from tulsa.learn.feature_groups import feature_groups
from tulsa.config import create_engine_from_config_file

import logging
import sys
import time
# take commandline arguments
import click
import json
# read constants


@click.command()
@click.argument('dbcreds',
                type=click.File('r'))
@click.argument('params_file',
                type=click.File('r'))
@click.option('--log-level', default='debug',
              type=click.Choice(['debug', 'info', 'warn']),
              help='set to "info" to avoid debugging information')
@click.option('--log-location', default=None,
              help='location to store log')
@click.option('--state-location', default='/mnt/data/tulsa/state',
              help="""location to store state_file keeping track of run numbers
                    usually where drake is doing this too""")
@click.option('--run-name', default='unnamed',
              help='the name to give this run, will be suffixed with a unique id too')
@click.option('--regenerate', is_flag=True,
              help='regenerate label and features, not read from Database')
@click.option('--report', default=None,
              type=click.Choice(['with_recs', 'standard']),
              help='''Save reports to CSVs after modeling
                      Set to "standard" to output risks
                      Set to "with_recs" to use experimental function that recommends
                              areas of improvement''')
def main(dbcreds, params_file, log_level, log_location, regenerate,
         run_name, state_location, report):
    """Run all the models!!!!

    You will need to specify the database credentials for DBCREDS and a
    parameter file as PARAMS_FILE.

    The format of DBCREDS is a json with the keys 'host', 'port', 'database',
    'user', and 'password' pointing to your postgres database.

    The format of your PARAMS_FILE is also a json which should look like
    the following::

        {
            "labels_to_make": ["eventualnot186_with2nd"],
            "feature_groups_to_make": ["reenroll"],
            "models_to_make": {
                "LR": { "penalty": ["l1"], "C": [0.01]},
                "RF": {"n_estimators": [1000], "max_depth": [50],
                       "max_features": ["log2"], "min_samples_split": [10]}
            },
            "metrics_to_make": [],
            "split_strategy": ["predict_new"],
            "scale": true
        }

    The potential values for each key are as follows:
        * labels_to_make: ['eventualnot186', 'eventualnot186_with2nd']
                                  see features.py for all options
        * feature_groups_to_make: ['all', 'map', 'actionable', ...]
                                  see feature_groups.py for all options
        * models_to_make: ['RF', 'LR', 'SVM', ...]
                                  see evaluate.py for all options
        * metrics_to_make: ['precision_at_{n}', 'recall_at_{n}', 'auc',
                             'prec_rec_n_graph', 'pred_probs_hist']
                                  see metrics.py for more information
        * split_strategy: ['cohort', 'predict_new']
                                  see splits.py for more information


    Note that each "model to make" takes a dictionary that is used by
    scikit-learn to make a ParameterGrid object. So if you only want to
    run a single model, all of the lists that appear should be of length one.
    """
    # implement logging
    numeric_level = getattr(logging, log_level.upper())

    logging_params = {'level': numeric_level,
                      'format': '%(asctime)s [%(levelname)s]: %(message)s'}
    if log_location:
        logging_params['filename'] = log_location
    else:
        logging_params['stream'] = sys.stderr

    logging.basicConfig(**logging_params)
    logging.info('Process started')
    logging.info('===============')
    start_time = time.time()

    params = json.load(params_file)
    labels_to_make = params['labels_to_make']
    feature_groups_to_make = params['feature_groups_to_make']
    models_to_make = params['models_to_make']
    metrics_to_make = params['metrics_to_make']
    split_strategies = params['split_strategy']
    try:
        scale = params['scale']
    except KeyError:
        scale = None
    # create engine
    engine = create_engine_from_config_file(dbcreds)

    # feature group mapping
    logging.info('feature groups requested are: %s', feature_groups_to_make)
    features_to_make = set()
    for group in feature_groups_to_make:
        features_to_make.update(feature_groups[group])
    features_to_make = list(features_to_make)
    logging.info('individual features to make are: %s', features_to_make)

    # instantiate a model
    for label_name in labels_to_make:
        tm = model.TulsaModel(engine,
                              features_to_make,
                              label_name,
                              models_to_make,
                              metrics_to_make,
                              split_strategies,
                              regenerate,
                              run_name,
                              state_location,
                              scale)

        logging.info('Initializing Tulsa model')

        tm.generate_labels()
        logging.info('Labels generated')

        tm.generate_features()
        logging.info('Features generated (%s features)', len(tm.label_feature_df.columns))

        tm.impute_missing_values()
        logging.info('imputed missing values')

        tm.warn_nans()
        logging.info('I tried to warn you about NaNs')

        tm.make_splits()
        logging.info('Make splits')

        tm.fit_models_and_metrics()
        logging.info('Model evaluated')

        tm.touch_run_number()
        logging.info('Touching run number')

        if report:
            logging.info('Reporting type is: %s', report)
            tm.report_predictions(report)
            logging.info('Reporting predictions to CSV')

    end_time = time.time()
    time_taken = end_time - start_time
    logging.info('Time taken: %s seconds', time_taken)
    logging.info('■  Done')


if __name__ == '__main__':
    main()
