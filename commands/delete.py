from vkbottle.bot import Blueprint, Message
import sys
sys.path.insert(0, '..')
from db.connect import collection 
bp = Blueprint()
from typing import Optional
from config.admins import admins
from config.super_admin import super_admin
from config.default_answer import *

exex = ['/delete <item>', '/DELETE <item>']

@bp.on.message(text=exex)
async def index(message: Message, item: Optional[str] = None):
    error_up = '/DELETE' in message.text
    cursor = collection.find({})
    b = []
    for i in cursor:
        b.append(i)
    if str(message.from_id) in admins or str(message.from_id) in super_admin:
        if item != None: 
            try:
                item = int(str(item))
            except:
                if (error_up):
                    await message.answer(prefix + error.upper())
                else:
                    await message.answer(error)

            if 'int' in str(type(item)):
                if item <= len(b) - 1:
                    abc = b[item]
                    id = abc['_id']
                    myquery = { "_id": id }
                    collection.delete_one(myquery)
                    if (error_up):
                        await message.answer(prefix + ok.upper())
                    else:
                        await message.answer(ok)
                else:
                    if (error_up):
                        await message.answer(prefix + error.upper())
                    else:
                        await message.answer(error)
            else:
                if (error_up):
                    await message.answer(prefix + error.upper())
                else:
                    await message.answer(error)
        else:
            if (error_up):
                await message.answer(prefix + error.upper())
            else:
                await message.answer(error)
    else:
        if (error_up):
            await message.answer(prefix + not_admin.upper())
        else:
            await message.answer(not_admin)