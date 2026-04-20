import dill
from sklearn.model_selection import GridSearchCV
from src.exception_handler import CustomException
import os
import sys 
from src.logger import logging
from sklearn.metrics import  mean_squared_error , median_absolute_error
import numpy as np


def save_object(file_path, preprocessor_obj):
    try: 
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(preprocessor_obj, file_obj)
    except Exception as e :
        raise CustomException(e,sys)


def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found at: {file_path}")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e :
        raise CustomException(e,sys)
    

def evalute_model(X_train , y_train , X_test , y_test , models , parameters):

    try:
        model_report = {}
        logging.info('Initiating the model evalutor pipeline')
        for i  in range(len(list(models))):
         
            model = list(models.values())[i]
            parameter = parameters[list(models.keys())[i]]

            gs = GridSearchCV(model, parameter, cv=5)
            logging.info('Applying the GridSearchCV on model : %s', model)
            gs.fit(X_train, y_train)

            logging.info('Training the model : %s', model)
            logging.info('Applying the model.fit on model')
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            logging.info('Model fitted successfully!')

            logging.info('Predictions for the train and test data ')
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            logging.info('Predictions on the train and test data done')


            logging.info('Evaluating the predictions on the different metrics')
            train_mse = mean_squared_error(y_train,y_pred_train)
            test_mse = mean_squared_error(y_test,y_pred_test)

            train_mae = median_absolute_error(y_train,y_pred_train)
            test_mae = median_absolute_error(y_test,y_pred_test)

            train_rmse = np.sqrt(train_mse)
            test_rmse = np.sqrt(test_mse)
            logging.info('Evaluations on differnt metrics completed')


            model_report[list(models.values())[i]] = {
                'Train MSE' : train_mse,
                'Test MSE' : test_mse,

                'Train RMSE' : train_rmse,
                'Test RMSE' : test_rmse,

                'Train MAE' : train_mae,
                'Test MAE' : test_mae,
          
            }

            return model_report


    except Exception as e :
        logging.info('Error Occured : %s', e)
        raise CustomException(e,sys)