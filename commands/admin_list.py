from vkbottle.bot import Blueprint, Message
import sys
sys.path.insert(0, '..')
from config.admins import admins
bp = Blueprint()
from config.default_answer import *

exex = ['/лист', '/ЛИСТ']

@bp.on.message(text = exex)
async def mem(message: Message):
    up = '/ЛИСТ' == message.text
    admin_string = ''
    for i in range(len(admins)):
        if i != len(admins) - 1:
            user = await bp.api.users.get(admins[i])
            name = user[0].first_name + ' ' + user[0].last_name
            admin_string += name + '\n'
        else:
            user = await bp.api.users.get(admins[i])
            name = user[0].first_name + ' ' + user[0].last_name
            admin_string += name
    if (up):
        await message.answer(prefix)
        await message.answer(admin_string.upper())
    else:
        await message.answer(admin_string)