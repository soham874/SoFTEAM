import logging
import json

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
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger