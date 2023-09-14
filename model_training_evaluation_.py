from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.preprocessing import  StandardScaler, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')
import joblib


def create_experiment(experiment_name, run_name, run_metrics):
    import mlflow
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        for metric, value in run_metrics.items():
            mlflow.log_metric(metric, value)

    print(f'Run - {run_name} is logged to Experiment - {experiment_name}')

def model_training_evaluation(df, folder_name, model_repo, features, experiment_name):
    
    def adjusted_r2_score(y_true, y_pred, n_samples, n_features):
        r2_src = r2_score(y_true, y_pred)
        adjusted_r2 = 1 - ((1 - r2_src) * (n_samples - 1)) / (n_samples - n_features - 1)
        return adjusted_r2

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
    
    # Hyperparameter through optuna
    # hyperparameter = (max_depth=8, learning_rate=0.40879878447497636, n_estimators=807, min_samples_split=9, min_samples_leaf=7,
    #     subsample=0.7433722037954684, max_features=0.6538785541124312, alpha=0.36434181881252864)
    step6 = GradientBoostingRegressor()

    pipe = Pipeline([
        ('step1', step1),
        ('step2', step2),
        ('step3', step3),
        ('step4', step4),
        ('step5', step5),
        ('step6', step6)
    ])
    
    pipe.fit(X_train, y_train)

    y_train_pred = pipe.predict(X_train)
    y_test_pred = pipe.predict(X_test)

    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_mse = mean_squared_error(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_r2 = r2_score(y_train, y_train_pred)
    train_r2_adj = adjusted_r2_score(y_train, y_train_pred, X_train.shape[0], X_train.shape[1])

    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_r2 = r2_score(y_test, y_test_pred)
    test_r2_adj = adjusted_r2_score(y_test, y_test_pred, X_test.shape[0], X_test.shape[1])
    
    kfold = KFold(n_splits=10, shuffle=True, random_state=42)
    score = cross_val_score(pipe, X_train, y_train, cv=kfold, scoring='r2')
    score_mean = score.mean()
    
    data = {'Train_MAE': train_mae, 'Train_MSE': train_mse, 'Train_RMSE' : train_rmse,
            'Train_R2_Score': train_r2, 'Train_Adj-R2_Score': train_r2_adj}

    file_path = os.path.join(folder_name, 'train_results.txt')
    with open(file_path, 'w') as txt_file:
        for key, value in data.items():
            txt_file.write(f'{key}: {value}\n')
            
    data = {'Test_MAE': test_mae, 'Test_MSE': test_mse, 'Test_RMSE' : train_rmse,
            'Test_R2_Score': train_r2, 'Test_Adj-R2_Score': train_r2_adj}

    file_path = os.path.join(folder_name, 'test_results.txt')
    with open(file_path, 'w') as txt_file:
        for key, value in data.items():
            txt_file.write(f'{key}: {value}\n')
            
    file_path = os.path.join(folder_name, 'cv_score.txt')
    with open(file_path, 'w') as txt_file:
        txt_file.write("Cross Validation Score: {}".format(score_mean))

    run_metrics = {"Train_MAE": train_mae, "Train_MSE": train_mse, "Train_RMSE": train_rmse, "Train_R2": train_r2, 
                   "Train_Adj-R2_Score": train_r2_adj,  "Test_MAE": test_mae, "Test_MSE": test_mse, "Test_RMSE": test_rmse,
                    "Test_R2": test_r2, "Test_Adj-R2_Score": train_r2_adj, "Cross-Validation_Score": score_mean}
    
    create_experiment(experiment_name, "First_Run", run_metrics)
        
    importances = pipe.named_steps['step6'].feature_importances_
    feature_imp_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    sor_feature_imp_df = feature_imp_df.sort_values('Importance', ascending=False)
    feature_importances = sor_feature_imp_df['Importance'].values
    feature_names = sor_feature_imp_df['Feature'].values

    data = {'Feature': feature_names,
            'Importance': feature_importances}
    df_plot = pd.DataFrame(data)

    plt.figure(figsize=(25, 10))
    sns.barplot(data=df_plot, x='Feature', y='Importance', palette='viridis')
    plt.title('Feature Importance')
    plt.xlabel('Feature')
    plt.ylabel('Importance')
    plt.xticks(rotation=-45)
    plt.savefig('{}/Feature_Importance_plot.png'.format(folder_name))
    plt.close()
 
    model_name = "xgboost_model.pkl"  
    model_filepath = os.path.join(model_repo, model_name)
    joblib.dump(pipe, model_filepath)