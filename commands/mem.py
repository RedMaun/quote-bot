from vkbottle.bot import Blueprint, Message
from os import popen
bp = Blueprint()
from config.default_answer import *

exex = ['/mem', '/MEM', '/memory', '/MEMORY']

@bp.on.message(text=exex)
async def mem(message: Message):
    if (message.text == '/mem' or message.text == '/memory'):
        memory = popen('neofetch memory | cut -c9-').read()
    else:
        memory = (popen('neofetch memory | cut -c9-').read()).upper()
        await message.answer(prefix+'\n') 
    await message.answer(memory)

