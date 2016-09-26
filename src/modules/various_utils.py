import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json

#5242880 = 5*1024*1024
def generateLogger(file_path, logger_name, max_file_size=5242880):
    logger_file_path=file_path
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    fileHandler = logging.FileHandler(logger_file_path)
    streamHandler = logging.StreamHandler()
    rotatingFileandler = RotatingFileHandler(logger_file_path, mode='a', maxBytes=max_file_size, 
                                     backupCount=2, encoding=None, delay=0)


    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.addHandler(rotatingFileandler)
    logger.setLevel(logging.DEBUG)

    return logger

def get_time_prefix():
    prefix = datetime.now().strftime('%y%m%d_%H%M%S')
    return prefix

def toJson(src):
    return json.dumps(src, default=dateHandler)

def dateHandler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()


