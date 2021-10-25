from vkbottle.bot import Blueprint, Message
from os import popen
bp = Blueprint()
from config.default_answer import *

exex = ['/uptime', '/UPTIME']

@bp.on.message(text=exex)
async def uptime(message: Message):
    if (message.text == '/uptime'):
        await message.answer(popen('neofetch uptime | cut -c9-').read())
    else:
        await message.answer(prefix+'\n') 
        await message.answer((popen('neofetch uptime | cut -c9-').read()).upper())