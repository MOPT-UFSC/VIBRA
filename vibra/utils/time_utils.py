import logging
from functools import wraps
from time import perf_counter


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        logging.info(f"{func.__name__} took {elapsed:.3f}s")
        return result

    return wrapper
