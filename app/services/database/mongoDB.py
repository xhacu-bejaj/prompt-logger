from dataclasses import dataclass
from pprint import pprint
from typing import Dict

from pymongo import MongoClient


from app.core.settings import settings
from app.models.schemas import QueryResponse



"""
MongoDB sends a dict where keys are strings, while the values are either: 
                                                                        - bson.objectid.ObjectId (_id attribute only)
                                                                        - string
                                                                        - list of strings (mongodb array)
"""

uri = settings.MONGODB_CONNECTION_STRING
client = MongoClient(uri)




#def send_query_to_mongo(llm_query):
try:
    db = client.get_database('articles_db')
    collection = db.get_collection('articles')

    query = {"authors":"Modan Tailleur"}
    author = collection.find(query) 
    print("#################")
    pprint(type(author))
    #client.close

except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)





































