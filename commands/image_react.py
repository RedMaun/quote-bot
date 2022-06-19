from vkbottle.bot import Blueprint, Message
import io
import aiohttp
from hashlib import blake2s
import os
from PIL import Image
import json
import pytesseract
import cv2
import matplotlib.pyplot as plt
from random import choice

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

config_content = config_load(config)

async def get_pic_by_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            img_bytes = await resp.read()
    filename = f'{blake2s(img_bytes).hexdigest()}.png'
    filepath = os.path.join(config_content['pics_dir'], filename)
    if not os.path.exists(filepath):
        with Image.open(io.BytesIO(img_bytes)) as img:
            img.save(filepath, 'PNG', save_all=True)
    return config_content['pics_dir'] + filename


async def get_photo(b):
    c = []
    for g in range(len(b)):
        c.append(b[g].height * b[g].width)
    url = b[c.index(max(c))].url
    return await get_pic_by_url(url)

@bp.on.message(func=lambda message: (message.attachments != []))
async def react(message: Message):
    neofetch_trigger = ['debian', 'uptime', 'gtk3', 'icons', 'neofetch', 'gnu/linux', 'x86_64', 'terminal', 'packages', 'intel', 'amd', 'kernel', 'shell', 'alpine', 'linux', 'apk', 'pkgs']
    img = await get_photo(message.attachments[0].photo.sizes)
    image = cv2.imread(img)
    string = pytesseract.image_to_string(image)
    string = string.lower()
    print(string)
    if (any(x in string for x in neofetch_trigger)):
        await message.reply(choice(('ХУЙНЯ', 'ХУЙНЯ!!!', 'Хуйня, переделывай.', 'вот кому-то делать нехуй')))

    