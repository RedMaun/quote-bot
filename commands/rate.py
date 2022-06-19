from vkbottle.bot import Blueprint, Message
from random import choice

bp = Blueprint()

handler = ['оцените', 'зацените', 'что думаете', 'чё думаете', 'че думаете', 'как вам?']

@bp.on.message(func=lambda message: any(x in message.text.lower() for x in handler))
async def hello_handler(message: Message):
    await message.reply(choice(('ХУЙНЯ', 'ХУЙНЯ!!!', 'Хуйня, переделывай.', 'вот кому-то делать нехуй')))
