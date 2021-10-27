import pymongo
import json

config = 'config.json'

with open(config, 'r') as f:
    data = json.load(f)

url = data["url"]

client = pymongo.MongoClient(url)
db = client.quote
collection = db.quotes