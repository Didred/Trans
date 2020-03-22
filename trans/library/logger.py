import logging
from functools import wraps


def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        try:
            logger.info("Function: %s\n" % func.__name__)
            logger.debug("args: %s\n" % format(args))
            logger.debug("kwargs: %s\n" % format(kwargs))
            result = func(*args, **kwargs)
            logger.debug("return: '%s'\n" % result)

            return result
        except Exception as exc:
            logger.exception(exc)
            raise

    return wrapper


def get_logger():
    return logging.getLogger("Tracker")
