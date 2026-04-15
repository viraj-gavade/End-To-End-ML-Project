import sys 



def error_message_details(error , error_details : sys ):
    _ , _ , exc_tb = error_details.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno
    error_message = f"\n Error occured in python file : {filename} \n At the line no : {line_no} \n Error : {error}"
    return error_message



class CustomException(Exception):
    def __init__(self,error_message , error_details):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_details)


    def __str__(self):
        return self.error_message
    


if __name__ == "__main__":
    try:
        a = 1 
        b = 0
        print(a/b)
    except Exception as e :
        raise CustomException(e,sys)
    