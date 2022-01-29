from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
import json
from typing import Optional
bp = Blueprint()
import string
abc = string.ascii_lowercase

config = 'chats.json'
defa = 'config.json'
def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/инициализация <item>', '/ИНИЦИАЛИЗАЦИЯ <item>', '/инит <item>', '/ИНИТ <item>'], description = 'initialisation of db in chat')

Init = Command()

@bp.on.message(text = Init.hdl())
async def initt(m: Message, item: Optional[str] = None):
    data = config_load(config)
    chats = data["chats"]
    default = config_load(defa)
    default = default["default"]
    c = 0
    if len(item) > 20:
        await Init.ans_up('Name must be < 20 symbols', m)
    else:
        c += 1

    for i in list(item):
        if not i in abc:
            await Init.ans_up('Name must be eng letter only without spaces', m)
            c -= 1
            break 
    c += 1
    if c == 2:
        try:
            _id = int(m.peer_id)
            if _id > 2000000000:
                _id = _id - 2000000000
                ids = []
                for i in range(len(chats)):
                    ids.append(list(chats[i].keys())[0])
                if str(_id) in ids:
                    await Init.ans_up('Already initialized', m)
                else:
                    chats.append({_id: item})
                    with open(config, 'w') as file:
                        json.dump(data, file)
                    await Init.ans_up(default["ok"], m)
            else:
                await Init.ans_up(default["error"], m) 
        except Exception as e:
            await Init.ans_up(e, m)
