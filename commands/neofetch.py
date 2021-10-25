from vkbottle.bot import Blueprint, Message
from os import popen
bp = Blueprint()
from config.default_answer import *

exex = ['/neofetch', '/NEOFETCH']

@bp.on.message(text=exex)
async def neofetch(message: Message):
    if (message.text == '/neofetch'):
        neo = popen('neofetch --disable shell --stdout').read()
    else:
        neo = (popen('neofetch --disable shell --stdout').read()).upper()
        await message.answer(prefix+'\n') 
    await message.answer(neo)