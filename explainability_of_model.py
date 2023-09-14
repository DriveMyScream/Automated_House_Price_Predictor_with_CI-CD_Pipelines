from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.preprocessing import  StandardScaler, RobustScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import shap
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

def model_explanability(df, folder_name, features):
    X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['price'], axis=1), df['price'], test_size=0.20, random_state=42)
    
    step1 = ColumnTransformer([
        ('ordinal_encoder', OrdinalEncoder(categories=[['Resale', 'New Property']]), [6])
    ], remainder='passthrough')

    step2 = ColumnTransformer([
        ('ohe_encoder', OneHotEncoder(drop='first', sparse_output=False), [8, 10])
    ], remainder='passthrough')

    step3 = ColumnTransformer([
        ('scaler', RobustScaler(), list(range(5, 60)))
    ], remainder='passthrough')

    step4 = ColumnTransformer([
        ('knn_imputer', KNNImputer(n_neighbors=3, weights='distance'), [5, 6, 7, 10])
    ], remainder='passthrough')

    step5 = ColumnTransformer([
        ('power_transform', PowerTransformer(method='yeo-johnson'), list(range(0, 60)))
    ], remainder='passthrough')

    pipe = Pipeline([
        ('step1', step1),
        ('step2', step2),
        ('step3', step3),
        ('step4', step4),
        ('step5', step5),
    ])

    X_train_trf = pipe.fit_transform(X_train, y_train)
    X_test_trf = pipe.transform(X_test)

    model = GradientBoostingRegressor()
    model.fit(X_train_trf, y_train)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train_trf)
    
    shap.summary_plot(shap_values, X_train_trf, feature_names=features, plot_type='bar')
    plt.savefig('{}/11_shap_summary_plot.png'.format(folder_name), bbox_inches='tight')
    plt.close()
    
    shap.summary_plot(shap_values, X_train_trf, feature_names=features)
    
    feature_idx = 0
    shap.dependence_plot(feature_idx, shap_values, X_train_trf, feature_names=features)
    
    shap.initjs()
    instance_idx = 0
    shap.plots.force(explainer.expected_value, shap_values[instance_idx], X_train_trf[instance_idx], feature_names = features)
    
    shap.plots.decision(explainer.expected_value, explainer.shap_values(X_train_trf), feature_order='importance', feature_names = features, ignore_warnings=True)
    
    shap.initjs()
    shap.force_plot(explainer.expected_value, shap_values[0:5,:], X_train_trf[0:5,:], plot_cmap="DrDb", feature_names=features)