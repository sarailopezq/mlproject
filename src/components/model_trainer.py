import os
import sys
from dataclasses import dataclass


from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging


from src.utils import save_object, evaluate_model

#for every component we need a config file

@dataclass
class ModelTrainerConfig: #whatever input we will need for our model training will be contained here
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig() #it will get inititalized, the path will be given

    def initiate_model_trainer(self, train_array, test_array):#, preprocessor_path):
        try:
            logging.info("Splitting training and test input data")
            #divide training and testing dataset
            X_train, y_train, X_test, y_test = (
                                                train_array[:, :-1],
                                                train_array[:, -1],
                                                test_array[:, :-1],
                                                test_array[:, -1]
                                                ) 
            #create dictionary of models:

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Classifier": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            # suggestion: try hyperparameter tunning
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "K-Neighbors Classifier": {
                    'n_neighbors': [5,7,9,11]
                    # 'weights' : ['uniform', 'distance']
                    # 'algorithm': ['ball_tree', 'kd_tree', 'brute']
                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }

            #create dictionary and create a function
            model_report:dict
            model_parameters:dict 
            model_report, model_parameters =evaluate_model(X_train = X_train, y_train = y_train, X_test = X_test, y_test = y_test, models = models, param = params) #function created in utils

            ## To get best model score from dict:
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict:
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_params = model_parameters[best_model_name] #added by me
            #best_model = models[best_model_name]
            best_model = models[best_model_name].set_params(**best_params) #added by me
            logging.info(f"Best model was {best_model_name}" ) ## added by me
            #logging.info(f"Best parameter set was {best_params}" ) ##added by me, didn't work

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            
            logging.info("Best found model on both training and testing dataset")

            #here you can load the pickle file
            #preprocessing_obj = load("preprocessor.pkl")

            #Save model in path:
            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            # the following values will be the displayed when executing the program
            #print(best_params) #added by me
            #print(best_model_name) #added by me
            #return r2_square
            print(model_report)#added by me
            #print(list(model_report.keys()))#added by me
            #print(list(model_report.values()))#added by me
            print(model_parameters)#added by me
            #print(list(model_parameters.values()))#added by me
            print(model_parameters['XGBRegressor'])#added by me
            return r2_square, best_model_name, best_params  #added by me


        except Exception as e:
            raise CustomException(e, sys)
        

