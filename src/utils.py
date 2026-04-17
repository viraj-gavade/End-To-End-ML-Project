import dill
from src.exception_handler import CustomException
import os
import sys 

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