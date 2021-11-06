from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from typing import Optional
import os
from vkbottle import PhotoMessageUploader
import json
from db.connect import collection
import random
import asyncio
from pyppeteer import launch

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command1(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/сь <item>', '/СЬ <item>', '/спокойной', '/СПОКОЙНОЙ'], description = 'display specific quote')

SL = Command1()

async def screenshit(id):
    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
    browser = await launch({'headless': True, 'defaultViewport': None})
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080, 'deviceScaleFactor':3})
    await page.goto('https://quote.redmaun.site/index/' + str(id))
    await page.waitForSelector('.cont'); 
    
    element = await page.querySelector('.cont')
    box = await element.boundingBox();
    x = box['x'] - 20;                                
    y = box['y'] - 20;                                
    w = box['width'] + 40;                            
    h = box['height'] + 40; 
    
    await page.screenshot({'path': '/tmp/{}.png'.format(str(id)), 'clip': {'x': x, 'y': y, 'width': w, 'height': h}})

    await browser.close()

    return await photo_uploader.upload('/tmp/{}.png'.format(str(id)))

@bp.on.message(text=SL.hdl())
async def index(m: Message, item: Optional[int] = None):
    cursor = collection.find({})
    quotes = []
    for i in cursor:
        quotes.append(i)
    if (m.text[:10].lower() == '/спокойной'):
        await SL.ans_up(quotes[17]["qu"], m)
    else:
        data = config_load(config)
        default = data["default"]
        try:
            item = int(item)
            if (isinstance(item, int) and item < len(quotes)):
                if (item != abs(item)):
                    item = len(quotes) - abs(item)

                if os.path.isfile('/tmp/{}.png'.format(str(item))):
                    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
                    att = await photo_uploader.upload('/tmp/{}.png'.format(str(item)))
                    await SL.ans_up('', m, att)
                else:
                    await SL.ans_up('', m, await screenshit(item))

            else:
                await SL.ans_up(default["error"], m)

        except Exception as err:
            await SL.ans_up(err, m)


class Command2(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/ведать', '/ВЕДАТЬ', '/random', '/RANDOM'], description = 'display random quote')

Random = Command2()

@bp.on.message(text=Random.hdl())
async def rrandom(m: Message):
    try:
        cursor = collection.find({})
        quotes = []
        for i in cursor:
            quotes.append(i)
        ind = random.randint(0, len(quotes)-1)
        photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
        
        if os.path.isfile('/tmp/{}.png'.format(str(ind))):
            photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
            att = await photo_uploader.upload('/tmp/{}.png'.format(str(ind)))
            await SL.ans_up('', m, att)
        else:
            await SL.ans_up('', m, await screenshit(ind))

    except Exception as err:
        await Random.ans_up(err, m)

