from pymongo import MongoClient
from pymongo.errors import OperationFailure
from config import config
from threading import Thread

class DbConnector:
    def __init__(self, db, collection):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[db]
        self.collection = self.db[collection]
        self.watcher = Thread(target=self.watch_collection)
        self.on_insert = None
        self.on_update = None
        self.on_delete = None
    
    def handle_on_insert(self, document):
        if self.on_insert:
            self.on_insert(document)

    def handle_on_insert(self, document):
        if self.on_update:
            self.on_update(document)

    def handle_on_delete(self, document):
        if self.on_delete:
            self.on_delete(document)

    def watch_collection(self, collection):
        try:
            with collection.watch() as stream:
                for change in stream:
                    if change["operationType"] == "insert":
                        self.handle_on_insert(change["fullDocument"])
                    if change["operationType"] == "update":
                        self.handle_on_update(change["fullDocument"])
                    if change["operationType"] == "delete":
                        self.handle_on_delete(change["fullDocument"])
        except OperationFailure as e:
            print("The change stream encountered an error: %s" % e) 


