from scipy.stats import kurtosis
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')
import scipy.stats as stats
import statsmodels.api as sm
from scipy.stats import norm

def statistical_analysis(df, folder_name):
    
    numerical_columns = df.select_dtypes(exclude=['object']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    num_describe = df.describe(include=['float64', 'int64'])
    file_name = 'Numerical_description.csv' 
    file_path = os.path.join(folder_name, file_name)
    num_describe.to_csv(file_path, index=False)
    
    cat_describe = df.describe(include=['object'])
    file_name = 'Categorical_description.csv' 
    file_path = os.path.join(folder_name, file_name)
    cat_describe.to_csv(file_path, index=False)

    def cofficient_of_variation(column):
      mean = column.mean()
      std_dev = column.std()
      return (std_dev / mean) * 100

    cv_data = {col: cofficient_of_variation(df[col]) for col in numerical_columns}
    cv_df = pd.DataFrame(cv_data, index=['Coefficient of Variation'])
    plt.figure(figsize=(25, 10))
    sns.barplot(data=cv_df)
    plt.title("Coefficient of Variation for Each Column")
    plt.xlabel('Columns')
    plt.ylabel('Coefficient of Variation (%)')
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.savefig('{}/Cofficient_of_variation_plot.png'.format(folder_name))
    plt.close()


    skewness_data = df[numerical_columns].skew()

    skewness_classification = []
    for skew_value in skewness_data:
      if skew_value > 0.5 and skew_value < 1:
        skew_type = "Right Skew"
      elif skew_value > -0.5 and skew_value < 0.5:
        skew_type = "Almost Symmetrical"
      elif skew_value < -0.5:
        skew_type = "Left Skew"
      skewness_classification.append(skew_type)

    plt.figure(figsize=(25, 10))
    sns.barplot(x=skewness_data.index.tolist(), y=skewness_data.values.tolist(), hue=skewness_classification)
    plt.title('Skewness Classification for Each Column')
    plt.xlabel('Columns')
    plt.ylabel('Skewness')
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.legend(title="Skewness Classification")
    plt.savefig('{}/Skewness_analysis_plot.png'.format(folder_name))
    plt.close()

    kurtosis_data = kurtosis(df[numerical_columns])

    kurtosis_ = []
    for value in kurtosis_data:
      if value > 0:
        type_ = "Peaked"
      elif value < 0:
        type_ = "Flat"
      else:
        type_ = "Similar to Normal"
      kurtosis_.append(type_)

    plt.figure(figsize=(25, 10))
    sns.barplot(x=numerical_columns, y=kurtosis_data.tolist(), hue=kurtosis_)
    plt.title('Kurtosis Classification for Each Column')
    plt.xlabel('Columns')
    plt.ylabel('Kurtosis')
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.legend(title="Kurtosis Classification")
    plt.savefig('{}/Kurtosis_analysis_plot.png'.format(folder_name))
    plt.close()