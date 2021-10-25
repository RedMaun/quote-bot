from vkbottle.bot import Blueprint, Message
import sys
sys.path.insert(0, '..')
from config.admins import admins
from config.super_admin import super_admin
from config.default_answer import *
bp = Blueprint()

exex = ['/admin', '/ADMIN']

@bp.on.message(text=exex)
async def mem(message: Message):
    up = '/ADMIN' == message.text
    try:
        if str(message.from_id) in admins or str(message.from_id) in super_admin:
            _id = message.reply_message.from_id
            user = await bp.api.users.get(_id)
            name = user[0].first_name + ' ' + user[0].last_name

            if (not (str(_id) in admins)):
                admins.append(str(_id))
                f = open('config/admins.py', 'w')
                f.write('admins = ' + str(admins)) 
                f.close()
                if (up):
                    await message.answer(prefix + str(name + ' теперь почетный член ВС ПИДР!').upper())
                else:
                    await message.answer(name + ' теперь почетный член ВС ПИДР!')
            else:
                if (up):
                    await message.answer(prefix + (name + ' уже оракул!').upper())
                else:
                    await message.answer((name + ' уже оракул!'))
        else:
            if (up):
                await message.answer(prefix + not_admin.upper())
            else:
                await message.answer(not_admin)
    except:
        if (up):
            await message.answer(prefix + error.upper())
        else:
            await message.answer(error)

