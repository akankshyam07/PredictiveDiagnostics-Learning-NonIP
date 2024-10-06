"""
Rajani Vanarse
Akankshya Mohanty
"""
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
from pymongo import MongoClient
from RuleEngine import Mongo_config
from RuleEngine.RuleConstants import RuleConstants


def write(database, collection, records):
    client = MongoConnection().get_instance()
    db = getattr(client, database)
    coll = getattr(db, collection)
    for record in records:
        coll.update({RuleConstants.ID : record[RuleConstants.ID]}, {'$set': record})


def read(database, collection, query_filter):
    client = MongoConnection().get_instance()
    db = getattr(client, database)
    coll = getattr(db, collection)
    result = coll.find(query_filter)
    return list(result)


class MongoConnection:
    _instance = None

    def __init__(self):
        MongoConnection._instance = MongoClient(host=Mongo_config.HOST, port=Mongo_config.PORT)

    @staticmethod
    def get_instance():
        if MongoConnection._instance is None:
            MongoConnection()
        return MongoConnection._instance

    @property
    def instance(self):
        return self.get_instance()
