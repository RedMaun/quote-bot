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
import numpy as np
import base64

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

config_content = config_load(config)

async def get_pic_by_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            img_str = await resp.read()

    nparr = np.fromstring(img_str, np.uint8)
    img_np = cv2.imdecode(nparr, flags=1)
    return img_np


async def get_photo(b):
    c = []
    for g in range(len(b)):
        c.append(b[g].height * b[g].width)
    url = b[c.index(max(c))].url
    return await get_pic_by_url(url)

@bp.on.message(func=lambda message: (message.attachments != []))
async def react(message: Message):
    neofetch_trigger = 'debian uptime gtk3 icons neofetch terminal packages kernel alpine linux apk pkgs'.split()
    code_trigger = 'div else include void main float printf def return append'.split()
    terminal_trigger = 'cat touch master rwx systemd systemctl wlan eth'.split()
    
    img = await get_photo(message.attachments[0].photo.sizes)
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    
    string_colorful = pytesseract.image_to_string(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    string_grey = pytesseract.image_to_string(img)

    string_colorful = string_colorful.lower()
    string_grey = string_grey.lower()

    string = string_colorful + string_grey
    string = string.split()
    print(string)

    if (any(x in string for x in neofetch_trigger)):
        await message.reply(choice(('ХУЙНЯ', 'ХУЙНЯ!!!', 'вот кому-то делать нехуй', 'найди работу, еблан', 'выйди на улицу', 'по тебе и видно + вот поэтому у тебя и нет девушки', 'да по тебе и видно', 'ну ты и долбаеб')))

    elif (any(x in string for x in code_trigger)):
        await message.reply(choice(('хуйня, переделывай', 'говнокод', 'ну ты и долбаеб', 'что за сьлржалсч', 'насрал в компилятор')))
    
    elif (any(x in string for x in terminal_trigger)):
        await message.reply(choice(('sudo rm -rf попробуй долбаёб', 'тебе не надоело?', 'надо было скачивать убунту')))

    
