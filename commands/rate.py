from vkbottle.bot import Blueprint, Message
from random import choice

bp = Blueprint()

@bp.on.message()
async def hello_handler(message: Message):
    if message.text.lower().startswith(('оцените', 'зацените')):
        await message.reply(choice(('ХУЙНЯ', 'ХУЙНЯ!!!', 'Хуйня, переделывай.')))
