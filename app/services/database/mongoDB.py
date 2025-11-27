

from pymongo import MongoClient


from app.core.settings import settings

uri = settings.MONGODB_CONNECTION_STRING
client = MongoClient(uri)


db = client.get_database('articles_db')
collection = db.get_collection('articles')

# query = {"authors":"Modan Tailleur"}
# author = collection.find_one(query)

# print(author['title']) # python complains but it works --> create sresponse chemas with pydantic






