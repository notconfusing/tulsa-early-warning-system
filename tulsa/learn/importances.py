"""
This is where we calculate feature importances for RF and LR
"""
import pandas as pd


def feature_importance(model_name, fitted_model, X_train, params):
    """
    :param model_name: the model name, one of 'LR', or 'RF'
    :param fitted_model: the model to extract importances from
    :param X_train: the df which has the feature column names
    :param params: the params used to generate the model
    :type model_name: str
    :type fitted_model: sklearn classifier
    :type X_train: pandas DataFrame
    :type params: dict
    :returns: pandas DataFrame like:
              ['model_name', 'feature_imp', 'feature_name', 'params']
    """
    # use feature_importances_ or coef_
    if model_name == 'RF':
        feat_imps = fitted_model.feature_importances_
    elif model_name == 'LR':
        feat_imps = fitted_model.coef_[0]
    feat_names = list(X_train.columns)
    fi_df = pd.DataFrame({'feat_imp': feat_imps,
                          'feat_name': feat_names})
    fi_df['model_name'] = model_name
    fi_df['params'] = str(params)
    return fi_df
