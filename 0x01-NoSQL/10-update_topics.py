#!/usr/bin/env python3
"""
Function that changes all topics of a school document based on the name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Update the topics of a school document based on its name.
    """
    # Update the document matching the name with the new topics
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
