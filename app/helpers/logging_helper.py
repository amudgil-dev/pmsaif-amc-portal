from flask import current_app
from functools import wraps

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_app.logger.debug(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def debug(message):
    current_app.logger.debug(message)

def info(message):
    current_app.logger.info(message)

    
def warning(message):
    current_app.logger.warning(message)

def error(message):
    current_app.logger.error(message)

def critical(message):
    current_app.logger.critical(message)

def log_exception(e):
    current_app.logger.exception(f"An exception occurred: {str(e)}")