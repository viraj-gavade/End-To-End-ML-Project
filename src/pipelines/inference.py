
import os 
import pickle
import pandas as pd


class InputDataSchema :
    def __init__(self , reading_score , writing_score , gender,race_ethnicity,parental_level_of_education,lunch , test_preparation_course ):
        self.reading_score = reading_score
        self.writing_score = writing_score
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.test_preparation_course = test_preparation_course
        self.lunch = lunch
    
    def get_data_as_frame(self):
        data = {
            'reading_score': [self.reading_score],
            'writing_score':[self.writing_score],
            'gender':[self.gender],
            'race_ethnicity': [self.race_ethnicity],
            'parental_level_of_education': [self.parental_level_of_education],
            'test_preparation_course':[ self.test_preparation_course],
            'lunch':[self.lunch]



        }

        return pd.DataFrame(data)



        

class InferencePipeline : 
    def __init__(self):
        self.model_path : str = os.path.join('artifacts','best_model.pkl')
        self.preprocessor_path : str = os.path.join('artifacts','preprocessor.pkl')

    def predict(self , features):

        with open(self.model_path , 'rb') as file : 
            model = pickle.load(file)

        with open(self.preprocessor_path , 'rb') as file :
            preprocessor = pickle.load(file)

        
        transformed_data = preprocessor.transform(features)

        result = model.predict(transformed_data)

        return result
    



    
