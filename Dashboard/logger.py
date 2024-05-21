import datetime
import os


class Logger:
    """
    A class for logging messages to a file.

    Args:
        log_file (str): The path to the log file.

    Attributes:
        log_file (str): The path to the log file.

    Example usage:
        logger = Logger("application.log")
        logger.info("This is an informational message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.custom("DEBUG", "This is a debug message.")
    """

    def __init__(self, log_file):
        self.log_file = log_file
        # Create the log file if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, 'w') as file:
                file.write("Log File Created\n")
    
    def write_log(self, level, message):
        """
        Write a log entry to the log file.

        Args:
            level (str): The log level (e.g., INFO, WARNING, ERROR).
            message (str): The log message.

        Returns:
            None
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as file:
            file.write(f"{timestamp} - {level} - {message}\n")
    
    def info(self, message):
        """
        Log an informational message.

        Args:
            message (str): The log message.

        Returns:
            None
        """
        self.write_log("INFO", message)
    
    def warning(self, message):
        """
        Log a warning message.

        Args:
            message (str): The log message.

        Returns:
            None
        """
        self.write_log("WARNING", message)
    
    def error(self, message):
        """
        Log an error message.

        Args:
            message (str): The log message.

        Returns:
            None
        """
        self.write_log("ERROR", message)
