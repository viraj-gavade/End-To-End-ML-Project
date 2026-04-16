import sys 
import os 
from src.exception_handler import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd 
from sklearn.model_selection import train_test_split



@dataclass
class DataIngestionConfig:
    train_data_path : str = os.path.join('artifacts','train.csv')
    test_data_path : str = os.path.join('artifacts','test.csv')
    raw_data_path : str = os.path.join('artifacts','raw.csv')



class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()


    def initiate_data_ingestion(self , file_path):
        try:
            logging.info('Initiating the data ingestion pipeline')
            logging.info('Reading the data from the data source ')
            df = pd.read_csv(file_path)

            logging.info('creating the artifacts directory')
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path),exist_ok=True)
            logging.info('artifacts folder created successfully')

            logging.info('Saving the raw data into the artifacts')
            df.to_csv(self.data_ingestion_config.raw_data_path,index=False,header=True)
            logging.info('Raw data file saved successfully to the artifacts folder')

            logging.info('Applying the train test split')
            train_set , test_set = train_test_split(df,test_size=0.2,random_state=60)
            logging.info('Train test split completed!')

            logging.info('Saving the train and test data to the artifacts folder')
            train_set.to_csv(self.data_ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_data_path,index=False,header=True)
            logging.info('train and test set saved to the to the artifacts folder')

            logging.info('Ingestion Pipeline excuted successfully!')
            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )

        except Exception as e :
            logging.info(e)
            raise CustomException(e,sys)
            


if __name__ == "__main__":
    ingestion_object = DataIngestion()
    train_path , test_path = ingestion_object.initiate_data_ingestion('notebooks\data\stud.csv')
    print('Train path : ' , train_path)
    print('Test Path : ' , test_path)

