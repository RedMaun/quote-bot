from vkbottle.bot import Blueprint, Message
from os import popen
bp = Blueprint()
from config.default_answer import *

exex = ['/test']

@bp.on.message(text=exex)
async def neofetch(m: Message):
    mes = await bp.api.messages.get_by_conversation_message_id(conversation_message_ids=m.reply_message.conversation_message_id, peer_id=m.peer_id)
    mes_get = mes.items[0]
    b = mes_get.attachments[0].photo.sizes
    c = []
    for i in range(len(b)):
        c.append(b[i].height*b[i].width)
    print(b[c.index(max(c))].url)