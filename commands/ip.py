from vkbottle.bot import Blueprint, Message
from os import popen
bp = Blueprint()
import sys
sys.path.insert(0, '..')
from config.super_admin import super_admin
from config.default_answer import *

exex = ['/ip', '/IP']

@bp.on.message(text=exex)
async def ip(message: Message):
    up = '/IP' == message.text
    if str(message.from_id) in super_admin:
        servip = popen('curl -s checkip.amazonaws.com').read()
        servip = 'ssh uzzer@' + str(servip)
        if (up):
            await message.answer(prefix+'\n') 
            await message.answer(servip.upper())
        else:
            await message.answer(servip)
    else:
        if (up):
            await message.answer(prefix + not_admin.upper())
        else:
            await message.answer(not_admin)