import sys 
import os 
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from src.logger import logging
from sklearn.preprocessing import StandardScaler
from src.exception_handler import CustomException
from sklearn.preprocessing import OneHotEncoder
from src.utils import save_object

class DataTransformationConfig : 
    preprocessor_object_path : str = os.path.join('artifacts','preprocessor.pkl')


class DataTranformation :
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_preprocessor_object(self):
        '''This function is responsible for creating the preprocessor object'''
        try : 
            logging.info('Intiating the preprocessor pipeline')

            numerical_columns = [ 'reading_score', 'writing_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            logging.info('Numerical Features Identified are : %s', numerical_columns)
            logging.info('Categorical Features Identified are : %s', categorical_columns)


            logging.info('Creating the numerical columns transformation pipeline')
            
            numerical_pipeline = Pipeline(
                steps=[
                    ('SimpleImputer',SimpleImputer(strategy='mean')),
                    ('StandardScalar' , StandardScaler(with_mean=False))
                ]
            )
            logging.info('numerical columns transformation pipeline created successfully')


        
            logging.info('Creating the categorical columns transformation pipeline')
            categorical_pipeline = Pipeline(
                steps=[
                    ('SimpleImputer',SimpleImputer(strategy='most_frequent')),
                    ('OneHotEncoder', OneHotEncoder()),
                    ('StandardScalar' , StandardScaler(with_mean=False))
                ]
            )
            logging.info('categorical columns transformation pipeline created successfully')


            logging.info('Applying the column transformer')
            preprocessor = ColumnTransformer(
                [
                    ('numerical_tranformer',numerical_pipeline , numerical_columns),
                    ('categorical_tranformer', categorical_pipeline , categorical_columns)
                ]
            )
            logging.info('Column transformer applied successfully !')
            logging.info('Preprocessor pipeline excuted successfully!!')

            return preprocessor
        except Exception as e :
            logging.info('Error Occured : %s', e)
            raise CustomException(e,sys)
        

    def initiate_data_tranformation(self , train_path , test_path):

        try :
            logging.info('Intiating the tranformation pipeline!')

            logging.info('Reading the train dataset')
            train_df = pd.read_csv(train_path)
            logging.info('train dataset read sucessfully!')

                
            logging.info('Reading the test dataset')
            test_df = pd.read_csv(test_path)
            logging.info('train dataset read sucessfully!')

            target_feature = 'math_score'
            
            logging.info('Creating the input and target features for the train dataset')
            input_feature_train_df = train_df.drop([target_feature],axis=1)
            target_feature_train_df = train_df[target_feature]
            logging.info('input and target features for the train dataset created sucessfully!')


            logging.info('Creating the input and target features for the test dataset')
            input_feature_test_df = test_df.drop([target_feature],axis=1)
            target_feature_test_df = test_df[target_feature]
            logging.info('input and target features for the test dataset created sucessfully!')

            logging.info('Loading the preprocessor object')
            preprocessor = self.get_preprocessor_object()
            logging.info(' preprocessor object loaded successfully!')


            logging.info('Applyin the transformation on the train and test data')

            input_feature_train = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train,np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test,np.array(target_feature_test_df)
            ]

            save_object(
                file_path = self.data_transformation_config.preprocessor_object_path,
                preprocessor_obj = preprocessor
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_object_path
            )
        except Exception as e :
            logging.info('Error Occured : %s', e)
            raise CustomException(e,sys)










