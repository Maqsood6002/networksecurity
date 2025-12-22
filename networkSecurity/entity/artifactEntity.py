from dataclasses import dataclass
from networkSecurity.entity.configEntity import DataIngestionConfig

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str