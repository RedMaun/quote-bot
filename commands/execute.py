from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
import json
from typing import Optional
from os import popen

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/e <item>', '/E <item>'], description = 'exec any command')

e = Command()

@bp.on.message(text=e.hdl())
async def ex(m: Message, item: Optional[str] = None):
    data = config_load(config)
    super_admin = data["super_admin"]
    
    if ('/E' == m.text[:2]):
        up = True
    else:
        up = False

    item = item.lower()
    
    try:
        if (item == 'neofetch'):
            await e.ans_up((popen('neofetch --disable shell --stdout').read()), m)

        elif (item == 'uptime'):
            await e.ans_up((popen('neofetch uptime | cut -c9-').read()), m)

        elif (item == 'time'):
            await e.ans_up((popen('date +"%H:%M %d/%m/%Y"').read()), m)

        elif (item == 'mem'):
            await e.ans_up((popen('neofetch memory | cut -c9-').read()), m)

        elif (item == 'ip' and m.from_id == super_admin):
            await e.ans_up((popen('curl -s checkip.amazonaws.com').read()), m)

        elif (m.from_id == super_admin):
            await e.ans_up((popen(str(item)).read()), m)

    except Exception as err:
        await e.ans_up(err, m)
    