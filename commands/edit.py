from vkbottle.bot import Blueprint, Message
import sys
sys.path.insert(0, '..')
from db.connect import collection 
bp = Blueprint()
from typing import Optional
from config.admins import admins
from config.super_admin import super_admin
from config.default_answer import *

exex = ['/edit <index> <item> <text>', '/EDIT <index> <item> <text>']

@bp.on.message(text=exex)
async def index(message: Message, index: Optional[str] = None, item: Optional[str] = None, text: Optional[str] = None):
    error_up = '/EDIT' in message.text
    if str(message.from_id) in admins or str(message.from_id) in super_admin:
        cursor = collection.find({})
        b = []
        for i in cursor:
            b.append(i)
        if index != None and item != None and text != None:
            try:
                index = int(str(index))
            except:
                if (error_up):
                    await message.answer(prefix + error.upper())
                else:
                    await message.answer(error)
            if 'int' in str(type(index)):
                if item == 'qu' or item == 'au' or item == 'link':                    
                    myquery = b[index]
                    id = myquery['_id']
                    if item == 'link':
                        try:
                            d = myquery[item]
                        except KeyError:
                            collection.update_one({'_id' : id}, {'$set' : {'link' : '' }})

                    if item == 'link' and text == 'empty':
                        collection.update_one({'_id' : id}, {'$set' : {'link' : '' }})
                        if (error_up):
                            await message.answer(prefix + ok.upper())
                        else:
                            await message.answer(ok)
                    else:
                        newvalues = { "$set": { item: text } }
                        collection.update_one({'_id' : id}, newvalues)
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
            await message.answer(prefix + not_admin.upper())
        else:
            await message.answer(not_admin)  