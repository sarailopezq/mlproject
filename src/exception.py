import sys #acces to variables of python environment
import logging
from src.logger import logging

#Whenever an error raises, this function is called:

def error_message_detail(error, error_detail:sys):
    #error detail is present inside of sys
    _,_, exc_tb = error_detail.exc_info() #on which file, line number the exception ocurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_error = exc_tb.tb_lineno
    error_text = str(error)
    error_message= "Error occured in python script name: [{0}], line number: [{1}], error message: [{2}]".format(file_name, line_error, error_text)
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail = error_detail)

    def __str__(self):
        return self.error_message
    

# if __name__ == "__main__":
#     try: 
#         a = 1/0
#     except Exception as e: 
#         logging.info("Divide by Zero")
#         raise CustomException(e, sys)

