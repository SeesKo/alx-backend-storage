#!/usr/bin/env python3
"""
Module provides functions for web interactions
including caching with Redis.
"""

import requests
import redis
import time
from functools import wraps
from typing import Callable

# Initialize Redis connection
redis_instance = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a function is called.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_instance.incr(count_key)
        return method(url)
    return wrapper


def cache_result(timeout: int) -> Callable:
    """
    Decorator to cache the result of a function with a timeout.
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            cache_key = f"cache:{url}"
            cached_result = redis_instance.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')
            else:
                result = method(url)
                redis_instance.setex(cache_key, timeout, result)
                return result
        return wrapper
    return decorator


@count_calls
@cache_result(timeout=10)
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a given URL.
    """
    response = requests.get(url)
    return response.text
