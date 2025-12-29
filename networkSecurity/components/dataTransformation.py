import sys
import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.entity.configEntity import DataTransformationConfig
from networkSecurity.entity.artifactEntity import DataTransformationArtifact, DataValidationArtifact
from networkSecurity.logging.logger import logging

from networkSecurity.constant.trainingPipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networkSecurity.utils.mainUtils.utils import save_numpy_array_data, save_object

class dataTransformation:
    def __init__(self,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    @staticmethod
    def get_data_transformer_object() -> Pipeline:
        imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
        preprocessing_pipeline = Pipeline(steps=[
            ('imputer', imputer)
        ])
        return preprocessing_pipeline

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"Reading training and testing data")
            train_df = dataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = dataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info(f"Splitting input and target features from training and testing data")
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            logging.info(f"Creating preprocessing pipeline")
            preprocessing_pipeline = dataTransformation.get_data_transformer_object()

            logging.info(f"Fitting and transforming training data")
            input_feature_train_arr = preprocessing_pipeline.fit_transform(input_feature_train_df)

            logging.info(f"Transforming testing data")
            input_feature_test_arr = preprocessing_pipeline.transform(input_feature_test_df)

            logging.info(f"Combining input features and target feature into single array for training and testing data")
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saving transformed training and testing arrays")
            transformed_train_file_path = self.data_transformation_config.transformed_train_file_path
            transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)
            logging.info(f"Saving preprocessing object")
            preprocessing_object_file_path = self.data_transformation_config.transformed_object_file_path
            save_object(file_path=preprocessing_object_file_path, obj=preprocessing_pipeline)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                transformed_object_file_path=preprocessing_object_file_path
            )
            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
