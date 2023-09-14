import os
import pandas as pd
import shutil
from datetime import datetime
import math
from scipy.stats import norm

def data_drift_detector(df, sample_df, folder_name):
    columns_names = df.select_dtypes(exclude=['object']).drop(columns=['price']).columns.tolist()
    mean_std_pop = df[columns_names].agg(['mean', 'std'])
    mean_std_sample = sample_df[columns_names].agg(['mean', 'std'])

    sample_size = len(sample_df)
    alpha = 0.05
    z_test_values = []
    for column_name in columns_names:
        ZScore = (mean_std_sample.loc['mean', column_name] - mean_std_pop.loc['mean', column_name]) / \
                 (mean_std_pop.loc['std', column_name] / math.sqrt(sample_size))
        
        critical_z = abs(norm.ppf(alpha / 2))
        if abs(ZScore) > critical_z:
            result = 'There is a difference'
        else:
            result = 'There is no difference'
        z_test_values.append({
            'Column': column_name,
            'ZScore': ZScore,
            'critical_z': critical_z,
            'Result': result})

    Z_test_results = pd.DataFrame(z_test_values)
    file_name = 'data_drift_results.csv'
    file_path = os.path.join(folder_name, file_name)
    Z_test_results.to_csv(file_path, index=False)