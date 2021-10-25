from vkbottle.bot import Blueprint, Message
from os import system
bp = Blueprint()
from config.super_admin import super_admin
import sys
sys.path.insert(0, '..')
from config.default_answer import *

exex = ['/stop', '/STOP']

@bp.on.message(text=exex)
async def stop(message: Message):
    if str(message.from_id) in super_admin:
        if (message.text == '/stop'):
            await message.answer('Выключение...')
        else:
            await message.answer(prefix + 'ВЫКЛЮЧАЮСЬ')
        system('systemctl restart dev')
        f = open('config/peer_id.py', 'w')
        f.write('peer_id = {}'.format(message.peer_id))
        f.close()
        system('systemctl stop bot')
    else:
        if (message.text == '/stop'):
            await message.answer(not_admin)
        else:
            await message.answer(prefix + not_admin.upper())