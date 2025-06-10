import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd 
import os

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder , StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


from src.exception_handler import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_object_file_path = os.path.join('artifact','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function  is responsible for data transformation
        '''
        try:
            numerical_features = ['writing_score','reading_score']
            
            categorical_feature = [
                'gender',
            'race_ethnicity',
            'parental_level_of_education',
            'lunch',
            'test_preparation_course',
            ]

            num_pipeline = Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scalar',StandardScaler())
                ]
            )

            logging.info('Numerical Columns scaling completed')

            cat_pipeline = Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('one_hot_endcoder',OneHotEncoder()),
                ('scalar',StandardScaler(with_mean=False))
                ]
            )

            logging.info('Categorical Columns encoding completed')

            preprocessor = ColumnTransformer(
                [
                    ('numerical_pipeline',num_pipeline,numerical_features),
                    ('categorical_pipeline',cat_pipeline,categorical_feature)
                ]
            )


            return preprocessor  

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('Data reading completed')

            logging.info('Obtaining preprocing object')
            preprocessor_obj = self.get_data_transformer_object()

            target_column_name = 'math_score'
            numerical_features = ['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info('Apllying the preprocessor object on train and test data')

            input_feature_train_array = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessor_obj.transform(input_feature_test_df)

            train_arr=np.c_[
                input_feature_train_array,np.array(target_feature_train_df)
            ]

            test_arr=np.c_[
                input_feature_test_array,np.array(target_feature_test_df)
            ]


            logging.info('saved preprocessing object')

            save_object(
                self.data_transformation_config.preprocessor_object_file_path,
                obj = preprocessor_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_object_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
            