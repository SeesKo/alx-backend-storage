#!/usr/bin/env python3
"""
Module provides functions for web interactions
including caching with Redis.
"""

import requests
import redis
import time

# Initialize Redis connection
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content from a URL and caches it with a TTL
    of 10 seconds. Also tracks the number of accesses to the URL.
    """
    # Check if content is cached
    cache_key = f"{url}:content"
    cached_content = redis_client.get(cache_key)

    if cached_content:
        # Increment access count
        redis_client.incr(f"count:{url}")
        return cached_content.decode('utf-8')

    # Fetch content from URL
    response = requests.get(url)
    html_content = response.text

    # Cache content with expiration time of 10 seconds
    redis_client.setex(cache_key, 10, html_content)

    # Increment access count
    redis_client.incr(f"count:{url}")

    return html_content
