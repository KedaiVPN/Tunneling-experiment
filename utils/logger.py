import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_dir = "logs"
        self._setup_logging()

    def _setup_logging(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Main logger
        self.logger = logging.getLogger('tunnel_server')
        self.logger.setLevel(logging.INFO)

        # File handler
        log_file = os.path.join(self.log_dir, f'tunnel_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)
