from vkbottle.bot import Blueprint, Message
import sys
sys.path.insert(0, '..')
from config.admins import admins
from config.super_admin import super_admin
from config.default_answer import *
bp = Blueprint()

exex = ['/del', '/DEL']

@bp.on.message(text=exex)
async def mem(message: Message):
    up = '/DEL' == message.text
    if str(message.from_id) in admins or str(message.from_id) in super_admin:
        _id = message.reply_message.from_id
        user = await bp.api.users.get(_id)
        name = user[0].first_name + ' ' + user[0].last_name
        if (not (str(_id) in admins) ):
            if (up):
                await message.answer(prefix + str(name + ' ' + ' не админ').upper())
            else:
                await message.answer(str(name + ' ' + ' не админ'))
        else:
            if len(admins) != 1:
                admins.pop(admins.index(str(_id)))
                f = open('config/admins.py', 'w')
                f.write('admins = ' + str(admins)) 
                f.close()
                if (up):
                    await message.answer(prefix + (name + ' более не является членом ПИДР').upper())
                else:
                    await message.answer((name + ' более не является членом ПИДР'))
            else:
                if (up):
                    await message.answer(prefix + 'Выбери нового БАЗМАНА перед уходом'.upper())
                else:
                    await message.answer('Выбери нового БАЗМАНА перед уходом')
    else:
        if (up):
            await message.answer(prefix + not_admin.upper())
        else:
            await message.answer(not_admin)


