#!/usr/bin/env python3
"""
Function that lists all documents in a collection.
"""


def list_all(mongo_collection):
    """
    List all documents in a MongoDB collection.
    """
    documents = mongo_collection.find({})
    return list(documents)
