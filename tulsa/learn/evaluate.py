"""
Module to run machine learning algorithms against model.

The module will take in the model split strategy and create the expected
test/train split groups for its respective scikit-learn's machine learning
algorithm.
"""
from tulsa.learn import metrics
from tulsa.learn.importances import feature_importance 

import logging
import time
from multiprocessing import cpu_count
import pandas as pd

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.grid_search import ParameterGrid
from sklearn.linear_model import LogisticRegression, Perceptron, SGDClassifier, OrthogonalMatchingPursuit, RandomizedLogisticRegression
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

clfs = {'LR': LogisticRegression(),
        'RF': RandomForestClassifier(),
        'ET': ExtraTreesClassifier(),
        'AB': AdaBoostClassifier(),
        'SVM': svm.SVC(),
        'GB': GradientBoostingClassifier(),
        'NB': GaussianNB(),
        'DT': DecisionTreeClassifier(),
        'SGD': SGDClassifier(),
        'KNN': KNeighborsClassifier()
        }


def fit_models_and_metrics(X_train, X_test, y_train, y_test, models_to_make,
                           metrics_to_make):
    """
    Runs all the models with the respective parameters and generates all
    the metrics.

    :returns: model metric results, and feat_imps, and feat_crosstab, and y_preds
    :rtype: list of tuples (model_name, params_list, metric_name,
            metric_value)
    """
    result_list = []
    feat_imp_df = pd.DataFrame()
    feat_crosstab = pd.DataFrame()
    y_preds_df = pd.DataFrame()

    # iterate ver model name and params
    for model_name, params_dict in models_to_make.items():
        clf = clfs[model_name]
        param_grid = ParameterGrid(params_dict)
        for params in param_grid:

            # try to multithread if possible
            try:
                n_jobs = cpu_count()
                clf.set_params(n_jobs=n_jobs, **params)
            except ValueError:
                clf.set_params(**params)

            logging.debug('classifier is %s', clf)

            # do the machine learning
            start_time = time.time()
            fitted_model = clf.fit(X_train, y_train)
            if hasattr(clf, 'predict_proba'):
                y_pred_probs = fitted_model.predict_proba(X_test)[:, 1]
                logging.info("I'm using predict_proba")
            else:
                y_pred_probs = fitted_model.decision_function(X_test)
                logging.info("I'm using decision_function")
            end_time = time.time()
            run_time = end_time - start_time

            # make metrics given y preds
            for metric_name in metrics_to_make:
                metric_value = metrics.make_metric(metric_name, y_pred_probs,
                                                   y_test, X_test, model_name, params)

                if ('crosstab_at_' in metric_name):
                    metric_value['model_name'] = model_name
                    feat_crosstab = feat_crosstab.append(metric_value)
                else:
                    model_metric_list = [model_name, params, metric_name, metric_value, run_time]
                    result_list.append(model_metric_list)

            # make feature importances if we can
            if model_name in ['RF', 'LR']:  # only things that support fi.
                curr_feat_imp_df = feature_importance(model_name,
                                                      fitted_model,
                                                      X_train,
                                                      params)
                feat_imp_df = feat_imp_df.append(curr_feat_imp_df)

            # export the predictions
            # but ONLY IF THE PARAM GRID IF LENGTH ONE.
            # so pretune your model, find the params you like
            # then get your preds.
            if len(param_grid) == 1:
                y_preds_df = pd.DataFrame(y_pred_probs, columns=['y_preds'])

    return result_list, feat_imp_df, feat_crosstab, y_preds_df
