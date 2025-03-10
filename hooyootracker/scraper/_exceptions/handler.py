from functools import wraps
from hooyootracker.logger import logger
from .custom_exceptions import (
    SourceScrapingError,
    DataExtractionError
)


def handle_source_exc(source_name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.error(SourceScrapingError(source_name), exc_info=True)
                return None
        return wrapper
    return decorator


def handle_data_extraction_exc(source_name=None, data_extraction_type=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.error(DataExtractionError(source_name, data_extraction_type), exc_info=True)
                return None
        return wrapper
    return decorator
