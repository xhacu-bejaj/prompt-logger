from pprint import pprint
from typing import Dict

from pymongo import MongoClient


from app.core.settings import settings
from app.models.schemas import QueryResponse

uri = settings.MONGODB_CONNECTION_STRING
client = MongoClient(uri)

#def check_mongodb_types(author):


"""
MongoDB sends a dict where keys are strings, while the values are either: 
                                                                        - bson.objectid.ObjectId (_id attribute only)
                                                                        - string
                                                                        - list of strings (mongodb array)

"""


#def send_query_to_mongo(llm_query):
try:
    db = client.get_database('articles_db')
    collection = db.get_collection('articles')

    query = {"authors":"Modan Tailleur"}
    author = collection.find_one(query) 
    
    # for key in author.keys():
    #     pprint(f"key: {key}, value type: {type(author[key])}")
    #     # if (type(author[key]) is list):
    #     #     for item in author[key]:
    #     #         pprint(f"attribute = {key}; list entry: {item}; list of: {type(item)}")  
    print("#################")
    pprint(author)
    client.close

except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)







