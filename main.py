from networkSecurity.components.dataIngestion import DataIngestion
from networkSecurity.components.dataValidation import DataValidation
from networkSecurity.components.dataTransformation import dataTransformation
from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.configEntity import DataIngestionConfig, DataTransformationConfig
from networkSecurity.entity.configEntity import DataValidationConfig
from networkSecurity.entity.configEntity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        logging.info("Starting data ingestion process")
        TrainingPipelineConfig=TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info(f"Data Ingestion completed successfully: {data_ingestion_artifact}")

        logging.info("Data validation process started")
        data_validation_config = DataValidationConfig(training_pipeline_config=TrainingPipelineConfig)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                          data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data validation completed successfully")

        logging.info("Data transformation process started")
        data_transformation_config = DataTransformationConfig(training_pipeline_config=TrainingPipelineConfig)
        data_transformation = dataTransformation(data_transformation_config=data_transformation_config,
                                                 data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        
    except NetworkSecurityException as e:
        logging.error(f"Data Ingestion failed: {e}")