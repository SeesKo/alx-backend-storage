#!/usr/bin/env python3
"""
Function that returns the list of school having a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve a list of schools that have a specific topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)
