from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from typing import Optional
import os
from vkbottle import PhotoMessageUploader
import json
from db.connect import db
import random
import asyncio
from pyppeteer import launch

bp = Blueprint()

chats = 'chats.json'
config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command1(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/сь <item>', '/СЬ <item>'], description = 'display specific quote')

SL = Command1()

async def screenshit(chat, id):
    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
    browser = await launch({'headless': True, 'defaultViewport': None})
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080, 'deviceScaleFactor':1})
    await page.goto('https://quote.redmaun.site/' + str(chat) + '/' + str(id))
    await page.waitForSelector('.cont'); 
    
    element = await page.querySelector('.cont')
    box = await element.boundingBox();
    x = box['x'] - 20;                                
    y = box['y'] - 20;                                
    w = box['width'] + 40;                            
    h = box['height'] + 40; 
    name = random.randint(1000000, 9999999)
    
    await page.screenshot({'path': '/tmp/{}.png'.format(str(name)), 'clip': {'x': x, 'y': y, 'width': w, 'height': h}})

    await browser.close()

    return await photo_uploader.upload('/tmp/{}.png'.format(str(name)))

@bp.on.message(text=SL.hdl())
async def index(m: Message, item: Optional[int] = None):
    chat = config_load(chats)
    chat = chat["chats"]

    temp = item.split(' ')
    if len(temp) == 1 and m.peer_id > 2000000000:
        item = temp[0]
        _id = m.peer_id - 2000000000
        ids = []
        for i in range(len(chat)):
            ids.append(str(*chat[i]))
        if str(_id) in ids:
            index = ids.index(str(_id))
            collection = db[chat[index][str(*chat[index])]]
            cchat = chat[index][str(*chat[index])]
    elif len(temp) == 2:
        _id, item = temp
        ids = []
        for i in range(len(chat)):
            ids.append( chat[i][ str(*chat[i]) ] )
        if str(_id) in ids:
            index = ids.index(str(_id))
            collection = db[chat[index][str(*chat[index])]]
            cchat = chat[index][str(*chat[index])]

    if collection != None:
        cursor = collection.find({})
        quotes = []
        for i in cursor:
            quotes.append(i)
        data = config_load(config)
        default = data["default"]
        try:
            item = int(item)
            if (isinstance(item, int) and item < len(quotes)):
                if (item != abs(item)):
                    item = len(quotes) - abs(item)

                await SL.ans_up('', m, await screenshit(cchat, item))

            else:
                await SL.ans_up(default["error"], m)

        except Exception as err:
            await SL.ans_up(err, m)


class Command2(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/ведать', '/ВЕДАТЬ', '/ведать <item>', '/ВЕДАТЬ <item>'], description = 'display random quote')

Random = Command2()

@bp.on.message(text=Random.hdl())
async def rrandom(m: Message, item: Optional[str] = None):
    try:
        chat = config_load(chats)
        chat = chat["chats"]

        if item == None:
            if m.peer_id > 2000000000:
                _id = m.peer_id - 2000000000
                ids = []
                for i in range(len(chat)):
                    ids.append(str(*chat[i]))
                if str(_id) in ids:
                    index = ids.index(str(_id))
                    collection = db[chat[index][str(*chat[index])]]
                    cchat = chat[index][str(*chat[index])]
                else:
                    cchat = chat[0]["0"]
                    collection = db[cchat]
            else:
                cchat = chat[0]["0"]
                collection = db[cchat]
        else:
            ids = []
            for i in range(len(chat)):
                ids.append( chat[i][ str(*chat[i]) ] )
            item = str(item)
            if item in ids:
                index = ids.index(item)
                cchat = chat[index][str(*chat[index])]
                collection = db[cchat]

        if collection:
            cursor = collection.find({})
            quotes = []
            for i in cursor:
                quotes.append(i)
            item = random.randint(0, len(quotes) - 1)
            data = config_load(config)
            default = data["default"]
            await SL.ans_up('', m, await screenshit(cchat, item))

    except Exception as err:
        await SL.ans_up(err, m)

