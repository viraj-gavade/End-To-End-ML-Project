import sys
import os
import pandas as pd
from src.exception_handler import CustomException
from src.logger import logging
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,features):
        try:
            # Use absolute path to ensure files are found
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            model_path = os.path.join(base_dir, 'artifact', 'model.pkl')
            preprocessor_path = os.path.join(base_dir, 'artifact', 'preprocessor.pkl')
            
            logging.info(f"Model path: {model_path}")
            logging.info(f"Preprocessor path: {preprocessor_path}")
            
            logging.info('Loading preprocessor and model')
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)
            
            logging.info('Transforming features using preprocessor')
            data_scaled = preprocessor.transform(features)
            
            logging.info('Making predictions using the model')
            predictions = model.predict(data_scaled)
            
            return predictions
        
        except Exception as e:
            logging.error(f"Error in prediction pipeline: {e}")
            raise CustomException(e, sys)



class CustomData:
    def __init__(self,gender:str,race_ethnicity:str,parental_level_of_education:str,lunch:str,test_preparation_course:str,writing_score:int,reading_score:int):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.writing_score = writing_score
        self.reading_score = reading_score


    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "writing_score": [self.writing_score],
                "reading_score": [self.reading_score]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Custom data converted to DataFrame')
            return df
        except Exception as e:
            logging.error(f"Error in converting custom data to DataFrame: {e}")
            raise CustomException(e, sys)
