from vkbottle.bot import Blueprint, Message
from os import popen
bp = Blueprint()
from config.default_answer import *

exex = ['/time', '/TIME']

@bp.on.message(text=exex)
async def time(message: Message):
    if (message.text == '/time'):
        date = popen('date +"%H:%M %d/%m/%Y"').read()
    else:
        date = (popen('date +"%H:%M %d/%m/%Y"').read()).upper()
        await message.answer(prefix+'\n') 
    await message.answer(date)