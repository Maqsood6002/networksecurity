from networkSecurity.components.dataIngestion import DataIngestion
from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.configEntity import DataIngestionConfig
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
    except NetworkSecurityException as e:
        logging.error(f"Data Ingestion failed: {e}")