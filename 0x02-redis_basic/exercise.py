#!/usr/bin/env python3
"""
Module provides a Cache class to interact with
Redis and store data with random keys.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


class Cache:
    """
    Cache class to interact with Redis for storing data with random keys.
    """

    def __init__(self):
        """
        Initialize the Redis connection and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in Redis with a random key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str,
        fn: Optional[Callable] = None
    ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve the data from Redis by key, and
        optionally apply a conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def count_calls(method: Callable) -> Callable:
        """Decorator to count how many times a method is called."""
        @wraps(method)
        def wrapped(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapped

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in Redis with a random key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
