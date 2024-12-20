import os
import sys

import numpy as np
import pandas as pd
import dill #library that will help us to load the pickle file, add it to requirements too

from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj) #the file will be saved in the specified path

    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}
        best_parameters = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            #apply grid search cross vaidation for paramaters
            #gs = GridSearchCV(model, para, cv = cv, n_jobs = n_jobs, verbose = verbose, refit = refit)
            gs = GridSearchCV(model, para, cv = 3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_) # desempaquetar diccionario
            #or ejemplo, si gs.best_params_ es {'param1': 10, 'param2': 0.01}, la línea model.set_params(**gs.best_params_) es equivalente a model.set_params(param1=10, param2=0.01).
            
            model.fit(X_train,y_train)
            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)
            
            best_parameters[list(models.keys())[i]] = gs.best_params_ ##added by me
            report[list(models.keys())[i]] = test_model_score

        return report, best_parameters

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try: 
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)


