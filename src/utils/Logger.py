import logging
import os
import platform

class Logger:
    logger = None
    def __init__(self, mode: int, log_file_name: str):
        # Determine the correct path based on the OS
        if platform.system() == 'Windows':
            base_path = os.getenv('LOCALAPPDATA', os.path.expanduser('~'))
            log_dir = os.path.join(base_path, 'Safe&Sound')
        else:
            base_path = os.path.expanduser('~')
            log_dir = os.path.join(base_path, '.local', 'share', 'Safe&Sound')

        # Ensure the directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Construct the full log file path
        log_file_path = os.path.join(log_dir, log_file_name)

        # Create the logger
        self.logger = logging.getLogger(__name__)
        
        # Set the logging level based on the mode integer value
        log_level = logging.DEBUG if mode == 1 else logging.INFO
        self.logger.setLevel(log_level)

        # Create file handler which logs to the specified file
        file_handler = logging.FileHandler(log_file_path, mode='a')
        file_handler.setLevel(log_level)

        # Define a formatter with detailed information in DEBUG mode
        if mode == 1:  # Debug mode
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s '
                                          '[%(filename)s:%(lineno)d - %(funcName)s()]')
        else:  # Info mode
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add the formatter to the file handler
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        if not self.logger.handlers:  # Prevent adding multiple handlers
            self.logger.addHandler(file_handler)

    
    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)
