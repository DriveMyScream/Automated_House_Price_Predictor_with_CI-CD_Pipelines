import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')

def Outler_Missing_value(df, folder_name):
    # Outlier
    numerical_columns = df.select_dtypes(exclude=['object']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    for column in numerical_columns:
        percentile25 = df[column].quantile(0.25)
        percentile75 = df[column].quantile(0.75)
        IQR = percentile75 - percentile25
        lower_limit = percentile25 - 1.5 * IQR
        upper_limit = percentile75 + 1.5 * IQR
        df[column] = np.where(df[column] > upper_limit,
                              upper_limit,
                               np.where(
                                df[column] < lower_limit,
                                lower_limit,
                                df[column]))
    
    
    data = {'25th_Percentile': percentile25, '75th_Percentile': percentile75, 
        'Upper_Limit': upper_limit, 'Lower_Limit': lower_limit}

    file_path = os.path.join(folder_name, 'data.txt')
    with open(file_path, 'w') as txt_file:
        for key, value in data.items():
            txt_file.write(f'{key}: {value}\n')
    
    # Missing value
    Missing_data = pd.DataFrame({'Missing count': df.isnull().sum(), 'Missing Percentage': (df.isnull().sum()/df.shape[0])*100})
    file_name = 'Missing_values.csv' 
    file_path = os.path.join(folder_name, file_name)
    Missing_data.to_csv(file_path, index=True)
    
    plt.figure(figsize=(15, 6))
    sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
    plt.savefig('{}/missing_value_plot.png'.format(folder_name))
    plt.close()
    
    df['furnished_status'].fillna("Not-Specified", inplace=True)
    plt.figure(figsize=(8, 4))
    plt.title("Count of different categories")
    sns.countplot(y='furnished_status', data=df);
    plt.savefig('{}/furnished_status.png'.format(folder_name))
    plt.close()
    
    return df