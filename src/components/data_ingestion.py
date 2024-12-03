import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass #use to create class variables

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig, ModelTrainer


# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent))

#inputs necessary for data ingestion, examples: where to save the data, where to save the raw data
# Any setting, any requirement  will be saved in class DataIngestionConfig:


@dataclass #it is a decorator, because inside a class to define the class variable you basically use __init__, 
#if you use  @dataclass you will be able to directly define your class variable
#output of the dataingestionconfig can be anything, a numpy error, a file saved in a folder, etc
#dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv") #in this folder, this file, the outputs will be created
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw.csv")
    

class DataIngestion:
    def __init__(self):  #this is actually not needed since we are useing the decorator, but if we have multiple functions within the class, then it is recommended to use __init__
        self.ingestion_config = DataIngestionConfig() #class variable or sub object

    def inititate_data_ingestion(self):
        #here goes the code for reading data from the databases
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True) #create it only when it exists

            df.to_csv(self.ingestion_config.raw_data_path, index = False, header = True)
            logging.info ("Train test split initiated")

            train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 42)
            
            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)
            logging.info ("Ingestion of data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            

        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    obj = DataIngestion()
    train_data, test_data = obj.inititate_data_ingestion()
    data_transformation = DataTransformation() #initialize data transformation
    #data_transformation.initiate_data_transformation(train_data, test_data)

    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))



    
