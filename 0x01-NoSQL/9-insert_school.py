#!/usr/bin/env python3
"""
Function that inserts a new document in a collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into a MongoDB collection
    based on keyword arguments.
    """
    # Insert the document with kwargs as its fields
    result = mongo_collection.insert_one(kwargs)

    # Return the _id of the newly inserted document
    return result.inserted_id
