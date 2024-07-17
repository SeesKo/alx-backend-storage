#!/usr/bin/env python3
"""
Module provides a Cache class to interact with
Redis and store data with random keys.
"""

import redis
import uuid
from typing import Callable, Optional, Union
import functools


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

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data as a UTF-8 string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data as an integer.
        """
        return self.get(key, fn=int)

    @staticmethod
    def replay(method: Callable) -> None:
        """
        Display the history of calls for a particular method.
        """
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        redis_instance = redis.Redis()
        inputs = redis_instance.lrange(inputs_key, 0, -1)
        outputs = redis_instance.lrange(outputs_key, 0, -1)

        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for i in range(len(inputs)):
            print(f"{method.__qualname__}{inputs[i].decode('utf-8')} -> "
                  f"{outputs[i].decode('utf-8')}")


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store history of inputs and outputs in Redis lists.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        # Store inputs as string representation
        self._redis.rpush(inputs_key, str(args))

        # Execute the original method
        result = method(self, *args, **kwargs)

        # Store output as string representation
        self._redis.rpush(outputs_key, str(result))

        return result

    return wrapper


# Apply decorators to the Cache.store method
Cache.store = call_history(Cache.store)
Cache.store = count_calls(Cache.store)
