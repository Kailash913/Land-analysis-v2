"""
Simple in-memory cache with TTL for async functions.
"""
import time
import hashlib
import json
from functools import wraps

_cache: dict = {}


def timed_cache(seconds: int = 3600):
    """Decorator that caches async function results for `seconds`."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build a cache key from function name + args
            key_data = f"{func.__module__}.{func.__name__}:{json.dumps(args, default=str)}:{json.dumps(kwargs, default=str)}"
            key = hashlib.md5(key_data.encode()).hexdigest()

            now = time.time()
            if key in _cache:
                value, timestamp = _cache[key]
                if now - timestamp < seconds:
                    return value

            result = await func(*args, **kwargs)
            _cache[key] = (result, now)
            return result

        return wrapper
    return decorator


def clear_cache():
    """Clear all cached values."""
    global _cache
    _cache.clear()
