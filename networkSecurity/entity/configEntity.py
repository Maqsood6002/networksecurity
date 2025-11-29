from datetime import datetime
import os
from networkSecurity.constant import trainingPipeline

print(trainingPipeline.ARTIFACTS_DIR)

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = trainingPipeline.PIPELINE_NAME
        self.artifact_name = trainingPipeline.ARTIFACTS_DIR
        self.artifacts_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifacts_dir, trainingPipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, trainingPipeline.DATA_INGESTION_FEATURE_STORE_DIR_NAME, trainingPipeline.FILE_NAME
        )

        self.train_file_path: str = os.path.join(
            self.data_ingestion_dir, trainingPipeline.DATA_INGESTION_INGESTED_DIR_NAME, trainingPipeline.TRAIN_FILE_NAME
        )

        self.test_file_path: str = os.path.join(
            self.data_ingestion_dir, trainingPipeline.DATA_INGESTION_INGESTED_DIR_NAME, trainingPipeline.TEST_FILE_NAME
        )

        self.train_test_split_ratio: float = trainingPipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = trainingPipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = trainingPipeline.DATA_INGESTION_DATABASE_NAME