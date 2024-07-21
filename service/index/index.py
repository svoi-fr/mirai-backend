from db.db_connector import DbConnector
from logging import getLogger
from time import sleep

class IndexService():
    def __init__(self):
        self.log = getLogger("index")
        self.store = DbConnector("index", "store")
        pass
    
    def log(self, message):
        self.log.info(message)
    
    def run(self):
        while True:
            jobs = self.store.collection.find({"indexed": False})
            for job in jobs:
                sleep(60)



if __name__ == "__main__":
    index = IndexService()
    index.run()



