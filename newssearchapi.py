
from pymongo import MongoClient
import re

class Newsearchapi(object):

    def __init__(self,key):
        print ("search for the {} new".format(key))
        #self.api_key = api_key

    def search_news(self, key=None):
        """
            News key to search on news content
		"""

        # Connect tp MongoDB database to search param
        try:
            conn = MongoClient()
        except:
            print("Could not connect to MongoDB")  # database

        # Connect to database
        db = conn.NewsScrapy

        # Created or Switched to collection names: newscollections
        collection = db.newscollections
        regx = re.compile("key", re.IGNORECASE)

        matches = collection.find_one({"text": regx})
        if not matches:
            titles = collection.find_one({"title": regx})
            print (titles)

        print (matches)