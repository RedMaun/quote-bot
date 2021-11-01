from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from db.connect import collection
from typing import Optional
import bson.json_util
import json

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/поиск <quote>', '/ПОИСК <quote>'], description = 'search db record')


Search = Command()

def parse_json(data):
    return json.loads(bson.json_util.dumps(data, ensure_ascii=False).encode('utf8'))

@bp.on.message(text = Search.hdl())
async def sear(m: Message, quote: Optional[str] = None):
    try:
        # cur1 = collection.find({"$text": {"$search": quote}}).limit(2)
        # cur = collection.find({ '$text': {"$search": {'index': 'text', 'text': {'query': quote}}} } ).limit(2)
        cur = collection.aggregate([ { '$search': { 'index': 'text', 'text': { 'query': quote, 'path': { 'wildcard': '*' } } } } ])
        cursor = collection.find({})
        quotes = []
        for i in cursor:
            quotes.append(i)
        
        b = []
        for i in range(len(quotes)):
            try:
                b.append(quotes[i]["qu"])
            except:
                b.append(None)
        
        qtes = []
        for i in cur:
            # if (isinstance(i["qu"], list)):
            #     for abc in i["qu"]:

            qtes.append('https://quote.redmaun.site/index/'+str(b.index(i["qu"])) + '\n' + str(i["qu"]))
        await Search.ans_up('\n\n'.join(qtes), m)

    except Exception as e:
        await Search.ans_up(e, m)



