import logging
from contextlib import contextmanager
from functools import wraps
from time import perf_counter


def function_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        logging.info(f"{func.__name__} took {elapsed:.3f}s")
        return result

    return wrapper


@contextmanager
def context_timer(name: str):
    start = perf_counter()
    yield start
    elapsed = perf_counter() - start
    logging.info(f"{name} took {elapsed:.3f}s")
