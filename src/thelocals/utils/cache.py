from functools import wraps


def async_cache(fn):
    cache = {}

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = await fn(*args, **kwargs)
        return cache[key]
    wrapper.cache = cache

    return wrapper
