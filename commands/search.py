from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from db.connect import collection
from typing import Optional
import bson.json_util
from iteration_utilities import deepflatten
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
            # print(i)
            if ("qu" in i and isinstance(i["qu"], dict) or "qu" in i and isinstance(i["qu"], list) and isinstance(list(deepflatten(i["qu"], ignore=dict))[0], dict)):
                c = list(deepflatten(i["qu"], ignore=dict))
                text = []
                for obj in c:
                    text.append(obj["text"])
                qtes.append('https://quote.redmaun.site/index/'+str(b.index(i["qu"])) + '\n' + '\n'.join(text))

            elif ("qu" in i and isinstance(i["qu"], list)):
                qtes.append('https://quote.redmaun.site/index/'+str(b.index(i["qu"])) + '\n' + '\n'.join(i["qu"]))

            elif isinstance("qu" in i and i["qu"], str):
                qtes.append('https://quote.redmaun.site/index/'+str(b.index(i["qu"])) + '\n' + str(i["qu"]))

        n = len('\n\n'.join(qtes))
        k = 4096
        if (n > k):
            symbols_per_message = int(k / len(qtes))
            if (symbols_per_message > 100):
                for i in range(len(qtes)):
                    if (len(qtes[i][:symbols_per_message -3]) != len(qtes[i])):
                        qtes[i] = qtes[i][:symbols_per_message - 1] + '…'
                    else:
                        qtes[i] = qtes[i][:symbols_per_message - 1]
            else:
                while symbols_per_message < 100:
                    qtes.pop(-1)
                    symbols_per_message = int(k / len(qtes))

                for i in range(len(qtes)):
                    if (len(qtes[i][:symbols_per_message -3]) != len(qtes[i])):
                        qtes[i] = qtes[i][:symbols_per_message - 1] + '…'
                    else:
                        qtes[i] = qtes[i][:symbols_per_message - 1]


        await Search.ans_up('\n\n'.join(qtes), m)

    except Exception as e:
        await Search.ans_up(e, m)
        



