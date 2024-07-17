#!/usr/bin/env python3
"""
Module provides a Cache class to interact with
Redis and store data with random keys.
"""

import redis
import uuid
from typing import Union


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
        """
        Store the data in Redis with a random key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
