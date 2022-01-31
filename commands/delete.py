from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from db.connect import db
from typing import Optional
import json

bp = Blueprint()

config = 'config.json'
chats = 'chats.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/delete <item>', '/DELETE <item>'], description = 'will delete quote')

Delete = Command()

@bp.on.message(text = Delete.hdl())
async def list(m: Message, item: Optional[int] = None, chat: Optional[str] = None, ):
    data = config_load(config)
    admins = data["admins"]
    default = data["default"]
    chat = config_load(chats)
    chat = chat["chats"]
    try:
        temp = item.split(' ')
        if len(temp) == 1:
            item = temp[0]
            _id = m.peer_id - 2000000000
            ids = []
            for i in range(len(chat)):
                ids.append(str(*chat[i]))
            if str(_id) in ids:
                index = ids.index(str(_id))
                collection = db[chat[index][str(*chat[index])]]
                cursor = collection.find({})
                quotes = []
                for i in cursor:
                    quotes.append(i)
                if (m.from_id in admins):
                    item = int(item)
                    if (item != None and isinstance(item, int)):
                        myquery = { "_id": quotes[item]['_id'] }
                        quote = collection.find_one(myquery)
                        collection_delete = db["delete"]
                        collection_delete.insert_one(quote)
                        collection.delete_one(myquery)
                        await Delete.ans_up(default['ok'], m)
                    else:
                        await Delete.ans_up(default['error'], m)
                else:
                    await Delete.ans_up(default['not_admin'], m)
            else:
                await Delete.ans_up(default['error'], m)

        elif len(temp) == 2:
            _id, item = temp

            ids = []
            for i in range(len(chat)):
                ids.append( chat[i][ str(*chat[i]) ] )
            if str(_id) in ids:
                index = ids.index(str(_id))
                collection = db[chat[index][str(*chat[index])]]
                cursor = collection.find({})
                quotes = []
                for i in cursor:
                    quotes.append(i)
                if (m.from_id in admins):
                    item = int(item)
                    if (item != None and isinstance(item, int)):
                        myquery = { "_id": quotes[item]['_id'] }
                        quote = collection.find_one(myquery)
                        collection_delete = db["delete"]
                        collection_delete.insert_one(quote)
                        collection.delete_one(myquery)
                        await Delete.ans_up(default['ok'], m)
                    else:
                        await Delete.ans_up(default['error'], m)
                else:
                    await Delete.ans_up(default['not_admin'], m)
            else:
                await Delete.ans_up(default['error'], m)

    except Exception as e:
        await Delete.ans_up(e, m)
        

