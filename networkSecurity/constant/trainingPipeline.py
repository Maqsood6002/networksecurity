import os
import sys
import numpy as np
import pandas as pd

#Common Constants
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACTS_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH: str = os.path.join("dataSchema","schema.yaml")

# Data Ingestion Constants
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurity"
DATA_INGESTION_DIR_NAME: str = "dataIngestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME: str = "featureStore"
DATA_INGESTION_INGESTED_DIR_NAME: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# Data Validation Constants
DATA_VALIDATION_DIR_NAME: str = "dataValidation"
DATA_VALIDATION_VALID_DIR_NAME: str = "validated"
DATA_VALIDATION_INVALID_DIR_NAME: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME: str = "driftReport"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"