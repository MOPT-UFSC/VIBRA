import builtins
import functools
import hashlib
import inspect


def preview_cache(func):
    source_code = inspect.getsource(func)
    func_hash = hashlib.md5(source_code.encode("utf-8")).hexdigest()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_store = getattr(builtins, "__HOT_RELOAD_CACHE__", {})

        key = (func.__name__, func_hash, args, frozenset(kwargs.items()))

        if key not in cache_store:
            cache_store[key] = func(*args, **kwargs)

        return cache_store[key]

    return wrapper
