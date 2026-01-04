import os
import sys

from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

from networkSecurity.components.dataTransformation import dataTransformation
from networkSecurity.components.modelTrainer import ModelTrainer
from networkSecurity.components.dataValidation import DataValidation
from networkSecurity.components.dataIngestion import DataIngestion

from networkSecurity.entity.configEntity import TrainingPipelineConfig, ModelTrainerConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networkSecurity.entity.artifactEntity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact

class trainingPipeline:
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig())
            logging.info(f"Data Ingestion Config: {data_ingestion_config}")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            data_validation_config = DataValidationConfig(training_pipeline_config=TrainingPipelineConfig())
            logging.info(f"Data Validation Config: {data_validation_config}")
            data_validation = DataValidation(data_validation_config=data_validation_config,
                                             data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            data_transformation_config = DataTransformationConfig(training_pipeline_config=TrainingPipelineConfig())
            logging.info(f"Data Transformation Config: {data_transformation_config}")
            data_transformation = dataTransformation(data_transformation_config=data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=TrainingPipelineConfig())
            logging.info(f"Model Trainer Config: {model_trainer_config}")
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e