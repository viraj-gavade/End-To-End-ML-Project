import sys 
import os 
from src.exception_handler import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd 
from sklearn.model_selection import train_test_split
from src.components.data_tranformation import DataTranformation
from src.components.model_trainer import ModelTrainer
from src.components.data_ingestion import DataIngestion



class TrainingPipeline: 
    def run_training_pipeline(self):
        ingestion_object = DataIngestion()
        train_path , test_path = ingestion_object.initiate_data_ingestion('notebooks/data/stud.csv')
        tranformation_object = DataTranformation()
        train_arr , test_arr , preprocessor_path = tranformation_object.initiate_data_tranformation(train_path, test_path)
        print('Train path : ' , train_arr)
        print('Test Path : ' , test_arr)
        model_trainer_object = ModelTrainer()
        best_model,best_model_name,test_score,path = model_trainer_object.initiate_model_training(train_arr,test_arr)
        logging.info('training pipeline complted')


if __name__== "__main__":
    TrainingPipeline().run_training_pipeline()


