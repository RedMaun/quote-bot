from vkbottle.bot import Blueprint, Message
from random import choice

bp = Blueprint()

@bp.on.message(func=lambda message: message.text.lower().startswith(('оцените', 'зацените', 'что думаете', 'чё думаете', 'че думаете', 'как вам?')))
async def hello_handler(message: Message):
    await message.reply(choice(('ХУЙНЯ', 'ХУЙНЯ!!!', 'Хуйня, переделывай.', 'вот кому-то делать нехуй')))
