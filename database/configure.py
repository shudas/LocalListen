"""
Configures the database(s) used by the application
"""
from config import config
from pymongo import MongoClient

# this db should be used for all db calls
db = None


def setup():
    global db
    # client = MongoClient(host=config.DB.mongo_host, port=int(config.DB.mongo_port))
    # db = client[config.DB.database]