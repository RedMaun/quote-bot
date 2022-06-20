from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
import json
import aiohttp
from PIL import Image, ImageFont, ImageDraw, ImageStat
import io
import os
from hashlib import blake2s
import random
from random import choice
from vkbottle import PhotoMessageUploader
import math

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

config_content = config_load(config)


class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/kernel5', 'KERNEL5','/kernel5.', '/KERNEL5.'], description = 'kernel 5.')

Kernel = Command()

async def get_pic_by_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            img_bytes = await resp.read()

    filename = f'{blake2s(img_bytes).hexdigest()}.png'
    filepath = os.path.join(config_content['pics_dir'], filename)

    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)

    img = Image.open(io.BytesIO(img_bytes))

    stat = ImageStat.Stat(img)
    gs = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)) 
            for r,g,b in img.getdata())
    brightness = sum(gs)/stat.count[0]

    if (brightness > 50):
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)

    width, height = img.size

    fontsize = 1
    img_fraction = 0.50
    fontlocation = '/home/uzzer/.fonts/Inter-Bold.ttf'
    font = ImageFont.truetype(fontlocation, fontsize)
    txt = choice(("kernel 5.", "KERNEL 5."))
    while font.getsize(txt)[0] < img_fraction*img.size[0]:
        fontsize += 1
        font = ImageFont.truetype(fontlocation, fontsize)

    fontsize -= 1
    
    font = ImageFont.truetype(fontlocation, random.randint((fontsize - 60 if fontsize > 60 else 20), fontsize+10))

    draw = ImageDraw.Draw(img)

    x = random.randint(0, width - font.getsize(txt)[0])
    y = random.randint(0, height - font.getsize(txt)[1])

    
    draw.text((x, y), txt, color, font=font)

    if not os.path.exists(filepath):
        img.save(filepath, 'png', save_all=True)
    return await photo_uploader.upload(filepath)

async def get_photo(b):
    c = []
    for g in range(len(b)):
        c.append(b[g].height * b[g].width)
    url = b[c.index(max(c))].url
    return await get_pic_by_url(url)

@bp.on.message(text=Kernel.hdl())
async def kernel(message: Message):
    try:
        if (message.reply_message):
            img = await get_photo(message.reply_message.attachments[0].photo.sizes)
        else:
            img = await get_photo(message.attachments[0].photo.sizes)
        
        await message.answer(attachment=img)
        
    except Exception as e:
        print(str(e))


    
    