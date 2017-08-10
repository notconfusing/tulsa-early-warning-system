from sklearn.metrics import precision_recall_curve, roc_auc_score
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tulsa.learn import helpers


def plot_precision_recall_n(y_true, y_prob, model_name, params, fig_dir='/mnt/data/tulsa/figs'):
    y_score = y_prob
    precision_curve, recall_curve, pr_thresholds = precision_recall_curve(y_true, y_score)
    precision_curve = precision_curve[:-1]
    recall_curve = recall_curve[:-1]
    pct_above_per_thresh = []
    number_scored = len(y_score)
    for value in pr_thresholds:
        num_above_thresh = len(y_score[y_score >= value])
        pct_above_thresh = num_above_thresh / float(number_scored)
        pct_above_per_thresh.append(pct_above_thresh)
    pct_above_per_thresh = np.array(pct_above_per_thresh)
    plt.clf()
    fig, ax1 = plt.subplots()
    ax1.plot(pct_above_per_thresh, precision_curve, 'b')
    ax1.set_xlabel('percent of population')
    ax1.set_ylabel('precision', color='b')
    ax2 = ax1.twinx()
    ax2.plot(pct_above_per_thresh, recall_curve, 'r')
    ax2.set_ylabel('recall', color='r')
    plt.title(model_name + ' \n ' + str(params))
    filepath = helpers.save_fig(plt, model_name, fig_dir=fig_dir)
    return filepath


def precision_recall_at_k(y_true, y_pred_probs, k, metric_type):
    """
    Returns either precision or recall at specified k, where k is proportion of total
    """
    threshold = np.sort(y_pred_probs)[::-1][int(k * len(y_pred_probs))]
    y_pred = np.asarray([1 if i >= threshold else 0 for i in y_pred_probs])
    return eval(metric_type + '_score')(y_true, y_pred)


def make_pred_probs_hist(y_pred_probs, model_name, params, fig_dir='/mnt/data/tulsa/figs/histograms'):
    """
    Makes histogram from predicted probabilities (if applicable) or
    decision function
    """
    plt.clf()
    plt.hist(y_pred_probs)
    plt.title(model_name + '\n' + str(params))
    plt.xlabel('probability')
    plt.ylabel('student count')
    filepath = helpers.save_fig(plt, model_name, fig_dir=fig_dir)
    return filepath


def feature_pred_crosstab(y_pred_probs, y_test, X_test, k, feature_list=['female', 'ethnicity___a', 'ethnicity___b', 'ethnicity___h', 'ethnicity___i', 'ethnicity___m', 'ethnicity___p', 'ethnicity___w']):
    threshold = np.sort(y_pred_probs)[::-1][int(k * len(y_pred_probs))]
    y_pred = np.asarray([1 if i >= threshold else 0 for i in y_pred_probs])
    y_test.name = 'y_actual'
    label_feature_pred_df = pd.concat([X_test.reset_index(), y_test.reset_index()], axis=1)
    label_feature_pred_df = label_feature_pred_df.rename(columns={0: 'y_pred'})
    feat_crosstab = pd.DataFrame()
    for feature in feature_list:
        try:
            feat_actual_crosstab = pd.crosstab(label_feature_pred_df[feature],
                                               y_test).apply(lambda r: r / r.sum(),
                                                             axis=1)
            feat_pred_crosstab = pd.crosstab(label_feature_pred_df[feature],
                                             y_pred).apply(lambda r: r / r.sum(),
                                                           axis=1)
            feat_actual_crosstab.reset_index(level=0, inplace=True)
            feat_pop_dist = label_feature_pred_df.groupby(feature).count().iloc[:,0]/len(label_feature_pred_df)
            this_feat_crosstab = pd.concat([pd.DataFrame([feature] * len(feat_pred_crosstab)),
                                            feat_actual_crosstab,
                                            feat_pred_crosstab,
                                            feat_pop_dist], axis=1)
            this_feat_crosstab.columns = ["feature_name", "feature_value", "actual_0", "actual_1", "pred_0", "pred_1", "population"]
            feat_crosstab = feat_crosstab.append(this_feat_crosstab)

        # the feature to crosstab was not in the dataframe
        except KeyError:
            logging.debug("I can't make the crosstab for %s cos you didn't give it to me", feature)
            pass
    return feat_crosstab


def make_metric(metric_name, y_pred_probs, y_true, X_test, model_name, params):
    # met_funs = {'precision_recall_curve': plot_precision_recall_n}
    if ('precision_at_' in metric_name) | ('recall_at_' in metric_name):
        k = float(str.split(metric_name, "_")[2]) / 100
        metric_type = str.split(metric_name, "_")[0]
        return precision_recall_at_k(y_true, y_pred_probs, k, metric_type)
    elif metric_name == 'pre_rec_n_graph':
        return plot_precision_recall_n(y_true, y_pred_probs, model_name, params)
    elif metric_name == 'auc':
        return roc_auc_score(y_true, y_pred_probs)
    elif metric_name == 'pred_probs_hist':
        return make_pred_probs_hist(y_pred_probs, model_name, params)
    elif ('crosstab_at_' in metric_name):
        k = float(str.split(metric_name, "_")[2]) / 100
        return feature_pred_crosstab(y_pred_probs, y_true, X_test, k)
    else:
        raise NotImplementedError
