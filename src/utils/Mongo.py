from pymongo import MongoClient


class Mongo:
    def __init__(self, url):
        client = MongoClient(url)
        self.db = client.horoscopeDb
