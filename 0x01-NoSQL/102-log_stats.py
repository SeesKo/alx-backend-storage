#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB.
"""
from pymongo import MongoClient


def log_stats():
    """ Provides statistics about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Total number of logs
    log_count = collection.count_documents({})
    print(f"{log_count} logs")

    # Methods stats
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Status check
    status_check_count = collection.count_documents({
        "method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    # Top 10 most present IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(collection.aggregate(pipeline))

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
