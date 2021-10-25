from vkbottle.bot import Blueprint, Message
import sys, os
sys.path.insert(0, '..')
from db.connect import collection 
bp = Blueprint()
from typing import Optional
from config.default_answer import *
from vkbottle import PhotoMessageUploader
from vkbottle.tools import DocMessagesUploader
import urllib.request

exex = ['/сь <item>', '/СЬ <item>']

@bp.on.message(text=exex)
async def index(message: Message, item: Optional[str] = None):
    cursor = collection.find({})
    if ('/сь' in message.text):
        error_mes = error
    else:
        error_mes = prefix + error.upper()
        
    b = []
    for i in cursor:
        b.append(i)
    try:
        item = int(str(item))
    except:
         await message.answer(error_mes)

    if 'int' in str(type(item)):
        if item >= len(b):
            await message.answer(error_mes)
        else:
            if os.path.isfile('/tmp/test.jpg'):
                os.remove('/tmp/test.jpg')
            if os.path.isfile('/tmp/test.gif'):
                os.remove('/tmp/test.gif')

            photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
            ind = item
            try:
                if ("'images':" in str(b[ind]) and "'qu':" in str(b[ind]) and b[ind]['images'] != []):
                    if os.path.isfile('/tmp/test.jpg'):
                        os.remove('/tmp/test.jpg')
                    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
                    doc_uploader = DocMessagesUploader(bp.api, generate_attachment_strings=True)

                    att = []
                    for url in b[ind]['images']:
                        if 'doc' in url:
                            urllib.request.urlretrieve(url, '/tmp/test.gif')
                            att.append(await doc_uploader.upload('test.gif', '/tmp/test.gif', peer_id=message.peer_id))
                        else:
                            urllib.request.urlretrieve(url, '/tmp/test.jpg')
                            att.append(await photo_uploader.upload('/tmp/test.jpg'))

                    if (message.text == '/RANDOM' or message.text == '/ВЕДАТЬ'):
                        if 'list' in str(type(b[ind]['qu'])):
                            await message.answer(prefix + (('\n'.join(b[ind]['qu'])).upper()), attachment=aatt)
                        else:
                            await message.answer(prefix + ((b[ind]['qu']).upper()), attachment=att)
                    else:
                        if 'list' in str(type(b[ind]['qu'])):
                            await message.answer(('\n'.join(b[ind]['qu'])), attachment=att)
                        else:
                            await message.answer((b[ind]['qu']), attachment=att)

                elif ("'qu':" in str(b[ind]) and not("'images':" in str(b[ind]))):
                    if (message.text == '/RANDOM' or message.text == '/ВЕДАТЬ'):
                        if 'list' in str(type(b[ind]['qu'])):
                            await message.answer(prefix + ('\n'.join(b[ind]['qu'])).upper())
                        else:
                            await message.answer(prefix + (b[ind]['qu']).upper())
                    else:
                        if 'list' in str(type(b[ind]['qu'])):
                            await message.answer('\n'.join(b[ind]['qu']))
                        else:
                            await message.answer(b[ind]['qu'])

                elif ("'images':" in str(b[ind]) and b[ind]['images'] != []):
                    if os.path.isfile('/tmp/test.jpg'):
                        os.remove('/tmp/test.jpg')
                    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
                    doc_uploader = DocMessagesUploader(bp.api, generate_attachment_strings=True)
                    att = []
                    for url in b[ind]['images']:
                        if 'doc' in url:
                            urllib.request.urlretrieve(url, '/tmp/test.gif')
                            att.append(await doc_uploader.upload('test.gif', '/tmp/test.gif', peer_id=message.peer_id))
                        else:
                            urllib.request.urlretrieve(url, '/tmp/test.jpg')
                            att.append(await photo_uploader.upload('/tmp/test.jpg'))

                    if (message.text == '/RANDOM' or message.text == '/ВЕДАТЬ'):
                        await message.answer(prefix, attachment=att)
                    else:
                        await message.answer(attachment=att)

                else:
                    if (message.text == '/RANDOM' or message.text == '/ВЕДАТЬ'):
                        await message.answer(prefix + error)
                    else:
                        await message.answer(error)

            except Exception as e:
                if (message.text == '/RANDOM' or message.text == '/ВЕДАТЬ'):
                    await message.answer(prefix + e.upper())
                else:
                    await message.answer(e) 