import os
import pandas as pd
import shutil
from datetime import datetime
from data_drift_detection import data_drift_detector 

def main():
    current_datetime = datetime.now()
    folder_name = current_datetime.strftime("%Y_%m_%d_%H_%M")
    os.makedirs(folder_name)

    data_drift_dir = "data_drift_results"
    model_expl_dir_path = os.path.join(data_drift_dir, folder_name)

    if not os.path.exists(model_expl_dir_path):
        shutil.copytree(folder_name, model_expl_dir_path)

    data_dir = "data_directory"
    filename = os.listdir(data_dir)[-1]
    filepath = os.path.join(data_dir, filename)
    df = pd.read_csv(filepath)
    sample_df = df.sample(30)

    data_drift_detector(df, sample_df, model_expl_dir_path)
    shutil.rmtree(folder_name)


if __name__ == "__main__":
    main()