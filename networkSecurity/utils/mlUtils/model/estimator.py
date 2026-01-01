from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

from networkSecurity.constant.trainingPipeline import SAVED_MODELS_DIR, MODEL_FILE_NAME
import os
import sys

class NetworkModel:
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model

    def predict(self, X):
        try:
            logging.info("Prediction started.")
            X_processed = self.preprocessor.transform(X)
            predictions = self.model.predict(X_processed)
            logging.info("Prediction completed.")
            return predictions
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
