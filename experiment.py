from pymongo import MongoClient
from app.core.settings import settings

uri = settings.MONGODB_CONNECTION_STRING
mongo_client = MongoClient(uri)

db = mongo_client.get_database('articles_db')
collection = db.get_collection('articles')

query_document = {"id": "5096000"}

mongo_response = collection.find(query_document)
print(f"mongo_response: {mongo_response.to_list()}")