import os 
import sys
from src.exception_handler import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet,
    BayesianRidge
)

from src.utils import save_object
from src.utils import evalute_model

@dataclass
class ModelTrainerConfig : 
    trained_model_path : str = os.path.join('artifacts','best_model.pkl')


class ModelTrainer : 
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    

    def initiate_model_training(self , train_array , test_array):
        logging.info('Initiating the model training pipeline')
        logging.info('Applying the train test split :  X_train , y_train , X_test , y_test ')
        X_train , y_train , X_test , y_test = (
            train_array[: , :-1],
            train_array[:,-1],
            test_array[:,:-1],
            test_array[:,-1]
        )
        logging.info('train test split :  X_train , y_train , X_test , y_test Applied successfully! ')

        logging.info('Creating the models dictonary')


        models = {
                    "Linear Regression": LinearRegression(),
                    "Ridge Regression": Ridge(alpha=1.0),
                    "Lasso Regression": Lasso(alpha=1.0),
                    "ElasticNet Regression": ElasticNet(alpha=1.0, l1_ratio=0.5),
                    "Bayesian Ridge Regression": BayesianRidge()
                    }
        
        parameters = {
            "Linear Regression": {},
            "Ridge Regression": {"alpha": [0.1, 1.0, 10.0]},
            "Lasso Regression": {"alpha": [0.1, 1.0, 10.0]},
            "ElasticNet Regression": {"alpha": [0.1, 1.0, 10.0], "l1_ratio": [0.1, 0.5, 0.9]},
            "Bayesian Ridge Regression": {}
        }



        logging.info('Creating the model_report dictonary')
        model_report : dict  = evalute_model(X_train , y_train , X_test , y_test , models , parameters)
        best_model_name = None
        best_model_score = float('inf')
        best_model_obj = None

    

        for model_obj in model_report:
            test_rmse = model_report[model_obj]['Test RMSE']
            if test_rmse < best_model_score:
                best_model_score = test_rmse
                best_model_obj = model_obj

        for name, model in models.items():
            if model == best_model_obj:
                best_model_name = name
                break

        best_model = models[best_model_name]
        test_score = model_report[best_model_obj]['Test RMSE']

        save_object(self.model_trainer_config.trained_model_path , best_model)

        return{
            'Best Model ' : best_model,
            'Best Model Name' : best_model_name,
            'Test RMSE' : test_score,
            'model path ' : self.model_trainer_config.trained_model_path

        }

        




