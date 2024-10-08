import logging
import json
import os

logging.basicConfig(level=logging.WARNING)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            'time': self.formatTime(record),
            'process': record.process,
            'file': record.filename,
            'line': record.lineno,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(data)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.propagate = False
    
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Create a file handler to log warnings and errors to a file
    file_handler = logging.FileHandler(f'Logs/info_{os.getpid()}.log')
    file_handler.setLevel(logging.DEBUG)  # Set to capture warnings and above

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s -  %(process)d - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger