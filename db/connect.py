import pymongo, sys
sys.path.insert(0, '..')
from config.db import url

client = pymongo.MongoClient(url)
db = client.quote
collection = db.quotes
