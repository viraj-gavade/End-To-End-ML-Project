import logging
import os 
import sys
from datetime import datetime
from src.exception import CustomException

LOG_FILE = f'{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log'
logs_path = os.path.join(os.getcwd(),"logs" , LOG_FILE)
os.makedirs(logs_path,exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


if __name__ == "__main__":
    logging.info('Logging has started !!')
    a = 1
    b = 0
    try:
        c = a/b
    except Exception as e:
        logging.info('Error has occured !!')
        raise CustomException(e,sys)
    