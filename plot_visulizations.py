import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')
from sklearn.decomposition import PCA

def visulizations(df, folder_name):
    
    numerical_columns = df.select_dtypes(exclude=['object']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    plt.figure(figsize=(10, 10))
    sns.scatterplot(x=df['latitude'], y=df['longitude'], hue=df['price'])
    plt.title('Latitude vs Longitude Scatterplot')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.savefig('{}/1_Map_visulization_plot.png'.format(folder_name))
    plt.close()

    num_rows = (len(numerical_columns) + 2) // 3
    num_cols = 3
    plt.figure(figsize=(20, 6 * num_rows))

    for i, column in enumerate(numerical_columns):
        plt.subplot(num_rows, num_cols, i+1)
        sns.scatterplot(x=df[column], y=df['price'])
        plt.title("Price vs {}".format(column), fontsize=14)
        plt.xlabel(column, fontsize=14)
        plt.ylabel("price", fontsize=14)

    plt.tight_layout()
    plt.savefig('{}/2_Scatter_plot.png'.format(folder_name))
    plt.close()
    

    num_rows = (len(numerical_columns) + 2) // 3
    num_cols = 3
    plt.figure(figsize=(20, 6 * num_rows))

    for i, column in enumerate(numerical_columns):
        if column in ['balcony', 'parking', 'lift']:
          plt.subplot(num_rows, num_cols, i+1)
          sns.histplot(x=df[column].fillna(0.1), bins=10, kde=True)
          plt.title(column, fontsize=14)
          plt.xlabel("Distrubution", fontsize=14)
          plt.ylabel("Count", fontsize=14)
        else:
          plt.subplot(num_rows, num_cols, i+1)
          sns.histplot(x=df[column], bins=10, kde=True)
          plt.title(column, fontsize=14)
          plt.xlabel("Distrubution", fontsize=14)
          plt.ylabel("Count", fontsize=14)

    plt.tight_layout()
    plt.savefig('{}/3_Histogram_plot.png'.format(folder_name))
    plt.close()

    num_rows = (len(numerical_columns) + 2) // 3
    num_cols = 3
    plt.figure(figsize=(20, 6 * num_rows))

    for i, column in enumerate(numerical_columns):
      plt.subplot(num_rows, num_cols, i+1)
      sns.boxplot(data=df[column])
      plt.title(column, fontsize=14)

    plt.tight_layout()
    plt.savefig('{}/4_Box_plot.png'.format(folder_name))
    plt.close()

    num_rows = (len(categorical_columns) + 2) // 3
    num_cols = 3
    plt.figure(figsize=(20, 6 * num_rows))

    for i, column in enumerate(categorical_columns):
      plt.subplot(num_rows, num_cols, i+1)
      sns.countplot(x=column, data=df)
      plt.title(column, fontsize=14)

    plt.tight_layout()
    plt.savefig('{}/5_Categorical_count_plot.png'.format(folder_name))
    plt.close()

    num_rows = (len(categorical_columns) + 2) // 3
    num_cols = 3
    plt.figure(figsize=(20, 6 * num_rows))
    for i, column in enumerate(categorical_columns):
      plt.subplot(num_rows, num_cols, i+1)
      palette_color = sns.color_palette('bright')
      plt.pie(x=df[column].value_counts() / df.shape[0] * 100, labels=df[column].value_counts().index.tolist(), autopct="%.0f%%")
      plt.title(column, fontsize=14)

    plt.tight_layout()
    plt.savefig('{}/6_Categorical_pie_plot.png'.format(folder_name))
    plt.close()

    pca = PCA(n_components=2, random_state=42)
    embedded_data = pca.fit_transform(df.drop(columns = ['neworold', 'furnished_status', 'balcony',  'type_of_building', 'parking', 'lift']).fillna(0.1))
    data = {'Dimension 1': embedded_data[:, 0],
            'Dimension 2': embedded_data[:, 1],
            'price': df['price']}
    df_plot = pd.DataFrame(data)
    
    plt.figure(figsize=(10, 10))
    sns.scatterplot(data=df_plot, x='Dimension 1', y='Dimension 2', hue='price', palette='viridis')
    plt.title('PCA Visualization')
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.savefig('{}/7_Pca_visualization.png'.format(folder_name))
    plt.close()

    correlation_matrix = df.corr(numeric_only=True)
    plt.figure(figsize=(20, 20))
    sns.heatmap(data=correlation_matrix, cmap='RdBu', annot=True, fmt=".2f", cbar=True)
    plt.title('Correlation Matrix')
    plt.xlabel('Feature')
    plt.ylabel('Feature')
    plt.savefig('{}/8_Correlation_matrix.png'.format(folder_name))
    plt.close()