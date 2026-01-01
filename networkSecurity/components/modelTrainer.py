import os
import sys
from networkSecurity.entity.configEntity import TrainingPipelineConfig, ModelTrainerConfig
from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.artifactEntity import ModelTrainerArtifact, ClassificationMetricArtifact, DataTransformationArtifact
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import accuracy_score
import pickle

from networkSecurity.utils.mlUtils.model.estimator import NetworkModel
from networkSecurity.utils.mainUtils.utils import load_numpy_array_data, save_object, load_object
from networkSecurity.utils.mlUtils.metric.classificationMetric import get_classification_score
from networkSecurity.utils.mainUtils.utils import evaluate_models

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "LogisticRegression": LogisticRegression(verbose=1),
            "KNeighborsClassifier": KNeighborsClassifier(),
            "DecisionTreeClassifier": DecisionTreeClassifier(),
            "RandomForestClassifier": RandomForestClassifier(verbose=1),
            "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
            "AdaBoostClassifier": AdaBoostClassifier()
        }

        params = {
            "LogisticRegression": {},
            "KNeighborsClassifier": {
                'n_neighbors': [3, 5, 7],
                'weights': ['uniform', 'distance']
            },
            "DecisionTreeClassifier": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                'max_depth': [None, 10, 20, 30]
            },
            "RandomForestClassifier": {
                'n_estimators': [8, 16, 32, 64, 128, 256],
                'max_depth': [None, 10, 20]
            },
            "GradientBoostingClassifier": {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1, 0.2, 0.5]
            },
            "AdaBoostClassifier": {
                'n_estimators': [8, 16, 32, 64, 128, 256],
                'learning_rate': [0.01, 0.1, 1.0, 0.5]
            }
        }

        model_report = evaluate_models(
            x_train=x_train, y_train=y_train,
            x_test=x_test, y_test=y_test,
            models=models, params=params
        )

        best_model_score = max(model_report.values())
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

        # Train metrics
        y_train_pred = best_model.predict(x_train)
        train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

        # Test metrics ✅ MOVED UP
        y_test_pred = best_model.predict(x_test)
        test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        preprocessor_obj = load_object(
            file_path=self.data_transformation_artifact.transformed_object_file_path
        )

        model_dir = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir, exist_ok=True)

        model_obj = NetworkModel(preprocessor=preprocessor_obj, model=best_model)
        save_object(
            file_path=self.model_trainer_config.trained_model_file_path,
            obj=model_obj
        )

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_matric_artifact=train_metric,
            test_matric_artifact=test_metric
        )

        logging.info(f"Best model found: {best_model_name} with score: {best_model_score}")

        return model_trainer_artifact

        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info(f"Loading transformed training data from: {train_file_path}")
            train_array = load_numpy_array_data(file_path=train_file_path)
            logging.info(f"Loading transformed testing data from: {test_file_path}")
            test_array = load_numpy_array_data(file_path=test_file_path)

            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            model_trainer_artifact = self.train_model(x_train=X_train, y_train=y_train, x_test=X_test, y_test=y_test)
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e