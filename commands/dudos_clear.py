from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from db.connect import collection
from typing import Optional
import json

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/dudos <item>'], description = 'clear shit from site after spam attack')

Dudos = Command()

@bp.on.message(text = Dudos.hdl())
async def list(m: Message, item: Optional[int] = None):
    data = config_load(config)
    admins = data["admins"]
    default = data["default"]
    cursor = collection.find({})
    quotes = []
    for i in cursor:
        quotes.append(i)
    try:
        if (m.from_id in admins):
            item = int(item)
            if (item != None and isinstance(item, int)):
                print(item)
                for i in range(item, len(quotes)):
                    myquery = { "_id": quotes[i]['_id'] }
                    print(i)
                    collection.delete_one(myquery)
                await Dudos.ans_up(default['ok'], m)
            else:
                await Dudos.ans_up(default['error'], m)
        else:
            await Dudos.ans_up(default['not_admin'], m)
    except Exception as e:
            await Dudos.ans_up(e, m)
