from dataclasses import dataclass
import datetime
from pprint import pprint
from typing import Dict

from bson import ObjectId
from pymongo import MongoClient


from app.core.settings import settings




"""
MongoDB sends a dict where keys are strings, while the values are either: 
                                                                        - bson.objectid.ObjectId (_id attribute only)
                                                                        - string
                                                                        - list of strings (mongodb array)
"""
@dataclass
class MongoDBHandler:
    uri = settings.MONGODB_CONNECTION_STRING
    mongo_client = MongoClient(uri)
    db = mongo_client.get_database('articles_db')
    collection = db.get_collection('articles')

def serialize_mongo_doc(doc):
    """Converts a MongoDB document to a JSON-serializable dictionary."""
    if isinstance(doc, dict):
        return {k: serialize_mongo_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_mongo_doc(i) for i in doc]
    elif isinstance(doc, datetime.datetime):
        return doc.isoformat()
    #elif isinstance(doc, ObjectId): # does not work, returns empty list, no errors at least
         #return str(doc)
    return doc




#def send_query_to_mongo(llm_query):
# try:
#     db = client.get_database('articles_db')
#     collection = db.get_collection('articles')

#     query = {"authors":"Modan Tailleur"}
#     author = collection.find(query) 
#     print("#################")
#     pprint(type(author))
#     #client.close

# except Exception as e:
#     raise Exception("Unable to find the document due to the following error: ", e)





































