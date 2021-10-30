from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from typing import Optional
import os
from time import sleep
from vkbottle import PhotoMessageUploader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from db.connect import collection
from PIL import Image
from io import BytesIO
import random

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver', options=options)

def make_screenshot(id):
    url = "https://quote.redmaun.site/index/{}".format(id)
    driver.get(url)
    sleep(4)
    e = driver.find_element_by_class_name("cont")
    size = e.size
    location = e.location

    w, h = size['width'], size['height']
    driver.set_window_size(1920, h*2)

    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png))

    left = location['x'] - 20
    top = location['y'] - 20
    right = location['x'] + size['width'] + 20
    bottom = location['y'] + size['height'] + 20

    name = random.randint(100000, 999999)
    im = im.crop((left, top, right, bottom)) 
    im.save('/tmp/{}.png'.format(str(name))) 
    return name

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/сь <item>', '/СЬ <item>'], description = 'display specific quote')

SL = Command()

@bp.on.message(text=SL.hdl())
async def help(m: Message, item: Optional[int] = None):
    cursor = collection.find({})
    quotes = []
    for i in cursor:
        quotes.append(i)
    
    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
    data = config_load(config)
    default = data["default"]
    try:
        item = int(item)
        if (isinstance(item, int) and item < len(quotes)):
            if (item == -1):
                item = len(quotes) - 1
            name = make_screenshot(item)
            if (name):
                att = await photo_uploader.upload('/tmp/{}.png'.format(str(name)))
                await SL.ans_up('', m, att)
            else:
                await SL.ans_up(default["error"], m)
        else:
            await SL.ans_up(default["error"], m)

    except Exception as err:
        await SL.ans_up(err, m)


