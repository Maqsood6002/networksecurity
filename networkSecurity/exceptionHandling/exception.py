import sys
from networkSecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self, error_message: Exception,error_detail: sys):
        _, _, exc_tb = sys.exc_info()

        self.error_message = str(error_message)
        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self) -> str:
        return (
            f"Error occurred in script: {self.file_name} "
            f"at line number: {self.line_number} "
            f"with message: {self.error_message}"
        )