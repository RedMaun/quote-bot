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
        super().__init__(handler = ['/сь <item>', '/СЬ <item>'], description = 'display specific quote')

SL = Command1()

@bp.on.message(text=SL.hdl())
async def index(m: Message, item: Optional[int] = None):
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
            if os.path.isfile('/tmp/{}.png'.format(str(item))):
                att = await photo_uploader.upload('/tmp/{}.png'.format(str(item)))
                await SL.ans_up('', m, att)
            else:
                browser = await launch({'headless': True})
                page = await browser.newPage()

                await page.goto('https://quote.redmaun.site/index/' + str(item))
                await page.waitForSelector('.cont'); 

                element = await page.querySelector('.cont')
                box = await element.boundingBox();
                # print(x, y, w, h)
                x = box['x'] - 20;                                
                y = box['y'] - 20;                                
                w = box['width'] + 40;                            
                h = box['height'] + 40; 
                
                # await element.screenshot({'path': '/tmp/{}.png'.format(str(ind))})
                await page.screenshot({'path': '/tmp/{}.png'.format(str(item)), 'clip': {'x': x, 'y': y, 'width': w, 'height': h}})

                await browser.close()

                att = await photo_uploader.upload('/tmp/{}.png'.format(str(item)))
                await SL.ans_up('', m, att)

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
            att = await photo_uploader.upload('/tmp/{}.png'.format(str(ind)))
            await SL.ans_up('', m, att)
        else:
            browser = await launch({'headless': True})
            page = await browser.newPage()

            await page.goto('https://quote.redmaun.site/index/' + str(ind))
            await page.waitForSelector('.cont'); 

            element = await page.querySelector('.cont')
            box = await element.boundingBox();
            # print(x, y, w, h)
            x = box['x'] - 20;                                
            y = box['y'] - 20;                                
            w = box['width'] + 40;                            
            h = box['height'] + 40; 
            
            # await element.screenshot({'path': '/tmp/{}.png'.format(str(ind))})
            await page.screenshot({'path': '/tmp/{}.png'.format(str(ind)), 'clip': {'x': x, 'y': y, 'width': w, 'height': h}})

            await browser.close()

            att = await photo_uploader.upload('/tmp/{}.png'.format(str(ind)))
            await SL.ans_up('', m, att)

    except Exception as err:
        await Random.ans_up(err, m)

