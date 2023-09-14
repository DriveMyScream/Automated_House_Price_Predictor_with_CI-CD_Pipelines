import os
import pandas as pd
import shutil
from datetime import datetime
from preprocessing import preprocess_dataframe
from handle_missing_value_outlier import Outler_Missing_value
from statistical_analysis_plot import statistical_analysis
from plot_visulizations import visulizations
from data_drift_detection import data_drift_detector
from model_training_evaluation_ import model_training_evaluation
from explainability_of_model import model_explanability

def main():
    current_datetime = datetime.now()
    folder_name = current_datetime.strftime("%Y_%m_%d_%H_%M")
    experiment_name = folder_name
    data_dir = "data_directory"
    oul_miss_dir = "handle_outlier_missing value"
    stat_dir = "data_statistics"
    vis_dir = "visualizations"
    model_reg = "model_repository"
    model_eval = "model_evaluation"
    model_expl = "model_explainability"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    source_path = folder_name
    oul_miss_dir_path = os.path.join(oul_miss_dir, folder_name)
    stat_dir_path = os.path.join(stat_dir, folder_name)
    vis_dir_path = os.path.join(vis_dir, folder_name)
    model_reg_dir_path = os.path.join(model_reg, folder_name)
    model_eval_dir_path = os.path.join(model_eval, folder_name)
    model_expl_dir_path = os.path.join(model_expl, folder_name)

    shutil.copytree(source_path, oul_miss_dir_path)
    shutil.copytree(source_path, stat_dir_path)
    shutil.copytree(source_path, vis_dir_path)
    shutil.copytree(source_path, model_reg_dir_path)
    shutil.copytree(source_path, model_eval_dir_path)
    shutil.copytree(source_path, model_expl_dir_path)
    shutil.rmtree(folder_name)


    features = ['area', 'latitude', 'longitude', 'bedrooms', 'bathrooms', 'balcony', 'parking', 'lift', 'Total_Rooms',
                'Approx_Avg_Area_Per_Room', 'Balcony_Ratio', 'Bathroom_Ratio', 'PD Hinduja Hospital', 'Lilavati Hospital',
                'Breach Candy Hospital', 'Wockhardt Hospital', 'KEM Hospital', 'JJ Hospital', 'Nair Hospital',
                'SevenHills Hospital', 'Nanavati Super Speciality Hospital', 'Kokilaben Dhirubhai Ambani Hospital',
                'St Xavier', 'Bombay Scottish', 'Don Bosco', 'Hansraj Morarji Public School', 'St Anne','KJ.Somaiya College',
                'Mithibai College', 'Ruia College', 'Jai Hind College', 'Narsee Monjee College', 'Fashion Street',
                'Bandra Linking Road', 'Bandra Hill Road', 'Colaba Causeway', 'Crawford Market', 'Malad West', 
                'Natraj Market', 'Hindmata', 'Grant Road', 'Infiniti Mall', 'RCity Mall', 'Phoenix Marketcity','Growel Mall', 
                'South Mumbai', 'Bandra', 'Juhu', 'Powai', 'BKC', 'Worli', 'Lower Parel', 'Andheri West', 'Goregaon East',
                'Thane', 'Not-Specified', 'Semi-Furnished', 'Unfurnished', 'Individual House', 'neworold']

    filename = [os.listdir(data_dir)][0][-3]      
    filepath = os.path.join(data_dir, filename)
    df = pd.read_csv(filepath)
    df = preprocess_dataframe(df)
    df = Outler_Missing_value(df, oul_miss_dir_path)
    statistical_analysis(df, stat_dir_path)
    visulizations(df, vis_dir_path)
    model_training_evaluation(df, model_eval_dir_path, model_reg_dir_path, features, experiment_name)
#    model_explanability(df, model_expl_dir_path, features)

if __name__ == "__main__":
    main()