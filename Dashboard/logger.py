import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, log_file=None):
        # Ensure the logs directory exists
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if log_file is None:
            log_file = datetime.datetime.now().strftime('%Y-%m-%d') + ".log"
        
        log_file_path = os.path.join(log_dir, log_file)
        self.logger = logging.getLogger("MyLogger")
        self.logger.setLevel(logging.INFO)
        handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1)
        handler.suffix = "%Y-%m-%d"
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)
        print(f"[INFO] {message}")

    def warning(self, message):
        self.logger.warning(message)
        print(f"[WARNING] {message}")

    def error(self, message):
        self.logger.error(message)
        print(f"[ERROR] {message}")