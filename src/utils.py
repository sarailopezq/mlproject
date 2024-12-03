import os
import sys

import numpy as np
import pandas as pd
import dill #library that will help us to create the pickle file, add it to requirements too

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj) #the file will be saved in the specified path

    except Exception as e:
        raise CustomException(e,sys)