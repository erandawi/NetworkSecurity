from networksecurity.enitiy.artifact_enitiy import DataIngestionArtifact, DataValidationArtifact
from networksecurity.enitiy.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file

from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd 
import os, sys

class DataValidation:
    def __inti___(self, data_ingestion_artifact: DataIngestionArtifact,
                data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame ha columns:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            ## validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain  all columns. \n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain  all columns. \n"
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        