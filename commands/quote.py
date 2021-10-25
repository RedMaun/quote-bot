from vkbottle.bot import Blueprint, Message
import sys
from datetime import date, datetime
sys.path.insert(0, '..')
from db.connect import collection 
bp = Blueprint()
from typing import Optional
from config.default_answer import *
import urllib.request

async def add_quote(audio, qu, au, link, link_mes, images):
    if (audio != None and qu != None or audio == None and qu == None and images == None or au == '' or audio == '' and qu == '' and images == '' or au == ''):
        return False
    today = date.today()
    d = today.strftime("%d.%m.%Y")
    t = str(datetime.now().time())[:5]
    time = d + ' в ' + t
    if (audio != None and link != None):
        data = {"audio": audio, "au": au, "da": time, "link": link}

    elif (audio != None):
         data = {"audio": audio, "au": au, "da": time}

    elif (qu != None and link != None and images != None):
        data = {"qu": qu, "au": au, "da": time, "link": link, "images": images}

    elif (link != None and images != None):
        data = {"au": au, "da": time, "link": link, "images": images}

    elif (qu != None and link != None):
        data = {"qu": qu, "au": au, "da": time, "link": link}

    elif (qu != None):
        data = {"qu": qu, "au": au, "da": time}

    else:
        return False

    abc = collection.insert_one(data)

    s = -1
    cursor = collection.find()
    for line in cursor:
        s += 1

    return link_mes + str(s)

exex = ['/сьлржалсч <text>', '/СЬЛРЖАЛСЧ <text>', '/сьлржалсч', '/СЬЛРЖАЛСЧ']

@bp.on.message(text=exex)
async def quote(message: Message, text: Optional[str] = None):
    if ('/сьлржалсч' in message.text):
        error_mes = error
        error_up = False
        link_mes = 'https://quote.redmaun.site:2087/index/'
    else:
        error_mes = prefix + error.upper()
        error_up = True
        link_mes = prefix + 'https://quote.redmaun.site:2087/index/'.upper()

    if (message.attachments != [] or text != None and text != ''):
        qu = text
        if (qu == None or qu != '' and qu[0] != '!' or qu == ''): 

            mes = await bp.api.messages.get_by_conversation_message_id(conversation_message_ids=message.conversation_message_id, peer_id=message.peer_id)
            mes_get = mes.items[0]
            images = []
            for i in range(len(mes_get.attachments)):
                if mes_get.attachments[i].doc:
                    images.append(mes_get.attachments[i].doc.url)
                else:
                    b = mes_get.attachments[i].photo.sizes
                    c = []
                    for g in range(len(b)):
                        c.append(b[g].height*b[g].width)
                    result = b[c.index(max(c))].url
                    images.append(result)
            
            if message.from_id == abs(message.from_id):
                user = await bp.api.users.get(message.from_id)
                au = user[0].first_name + ' ' + user[0].last_name
                link = 'https://vk.com/id{}'.format(message.from_id)
            else:
                group = await bp.api.groups.get_by_id(message.group_id)
                au = group[0].name
                link = 'https://vk.com/public{}'.format(message.group_id)

            ans = await add_quote(None, qu, au, link, link_mes, images)
            if (ans != False):
                await message.answer(ans)
            else:
                await message.answer(error_mes)
        else:
            await message.answer(error_mes)
        
    else:
        if message.reply_message != None:
                if message.reply_message.attachments != []:
                    if message.reply_message.attachments[0].audio_message:
                        try:
                            audio = message.reply_message.attachments[0].audio_message.link_mp3
                            if message.reply_message.from_id == abs(message.reply_message.from_id):
                                user = await bp.api.users.get(message.reply_message.from_id)
                                au = user[0].first_name + ' ' + user[0].last_name
                                link = 'https://vk.com/id{}'.format(message.reply_message.from_id)
                            else:
                                group = await bp.api.groups.get_by_id(message.group_id)
                                au = group[0].name
                                link = 'https://vk.com/public{}'.format(message.group_id)
                            ans = await add_quote(audio, None, au, link, link_mes, None)
                            if (ans != False):
                                await message.answer(ans)
                            else:
                                await message.answer(error_mes)
                        except Exception as e:
                            if (error_up):
                                await message.answer(prefix + e.upper())
                            else:
                                await message.answer(e)                           
                    else:
                        qu = message.reply_message.text
                        if (qu != '' and qu[0] != '!' or qu == ''): 
                            try:
                                if message.reply_message.from_id == abs(message.reply_message.from_id):
                                    user = await bp.api.users.get(message.reply_message.from_id)
                                    au = user[0].first_name + ' ' + user[0].last_name
                                    link = 'https://vk.com/id{}'.format(message.reply_message.from_id)
                                else:
                                    group = await bp.api.groups.get_by_id(message.group_id)
                                    au = group[0].name
                                    link = 'https://vk.com/public{}'.format(message.group_id)
                                
                                images = []
                                mes = await bp.api.messages.get_by_conversation_message_id(conversation_message_ids=message.reply_message.conversation_message_id, peer_id=message.peer_id)
                                mes_get = mes.items[0]
                                for i in range(len(mes_get.attachments)):
                                    if mes_get.attachments[i].doc:
                                        images.append(mes_get.attachments[i].doc.url)
                                    else:
                                        b = mes_get.attachments[i].photo.sizes
                                        c = []
                                        for g in range(len(b)):
                                            c.append(b[g].height*b[g].width)
                                        result = b[c.index(max(c))].url
                                        images.append(result)

                                if (images != []):
                                    ans = await add_quote(None, qu, au, link, link_mes, images)
                                else:
                                    ans = await add_quote(None, qu, au, link, link_mes, None)

                                if (ans != False):
                                    await message.answer(ans)
                                else:
                                    await message.answer(error_mes)
                            except Exception as e:
                                if (error_up):
                                    await message.answer(prefix + e.upper())
                                else:
                                    await message.answer(e)  
                        else:
                            await message.answer(error_mes)
                else:
                    qu = message.reply_message.text
                    if qu != '' and qu[0] != '!': 
                        try:
                            if message.reply_message.from_id == abs(message.reply_message.from_id):
                                user = await bp.api.users.get(message.reply_message.from_id)
                                au = user[0].first_name + ' ' + user[0].last_name
                                link = 'https://vk.com/id{}'.format(message.reply_message.from_id)
                            else:
                                group = await bp.api.groups.get_by_id(message.group_id)
                                au = group[0].name
                                link = 'https://vk.com/public{}'.format(message.group_id)

                            ans = await add_quote(None, qu, au, link, link_mes, None)
                            if (ans != False):
                                await message.answer(ans)
                            else:
                                await message.answer(error_mes)
                        except Exception as e:
                            if (error_up):
                                await message.answer(prefix + e.upper())
                            else:
                                await message.answer(e)  
                    else:
                        await message.answer(error_mes)
        else:
            try:
                if message.fwd_messages[0].attachments[0].audio_message:
                    audio = message.fwd_messages[0].attachments[0].audio_message.link_mp3
                    if message.reply_message.from_id == abs(message.reply_message.from_id):
                        user = await bp.api.users.get(message.reply_message.from_id)
                        au = user[0].first_name + ' ' + user[0].last_name
                        link = 'https://vk.com/id{}'.format(message.reply_message.from_id)
                    else:
                        group = await bp.api.groups.get_by_id(message.group_id)
                        au = group[0].name
                        link = 'https://vk.com/public{}'.format(message.group_id)
                    ans = await add_quote(audio, None, au, link, link_mes, None)
                    if (ans != False):
                        await message.answer(ans)
                    else:
                        await message.answer(error_mes)
                else:
                    if len(message.fwd_messages) != 0:
                        a = 0
                        for i in range(len(message.fwd_messages)):
                            if message.fwd_messages[i].text != '' and message.fwd_messages[i].text[0] == '!':
                                a = 1
                        if a == 0:
                            try:
                                check = []
                                qu = []
                                link = ''
                                for i in range(len(message.fwd_messages)):
                                    if message.fwd_messages[i].from_id == abs(message.fwd_messages[i].from_id):
                                        user = await bp.api.users.get(message.fwd_messages[i].from_id)
                                        check.append(str(user[0].first_name + ' ' + user[0].last_name))
                                    else:
                                        group = await bp.api.groups.get_by_id(abs(message.fwd_messages[i].from_id))
                                        check.append(str(group[0].name))
                                if (check.count(check[0]) == len(check)):
                                    if message.fwd_messages[0].from_id == abs(message.fwd_messages[0].from_id):
                                        user = await bp.api.users.get(message.fwd_messages[0].from_id)
                                        for i in range(len(message.fwd_messages)):
                                            qu.append(message.fwd_messages[i].text)
                                        au = user[0].first_name + ' ' + user[0].last_name
                                        link = 'https://vk.com/id{}'.format(message.fwd_messages[0].from_id)
                                    else:
                                        group = await bp.api.groups.get_by_id(abs(message.fwd_messages[0].from_id))
                                        for i in range(len(message.fwd_messages)):
                                            qu.append(message.fwd_messages[i].text)
                                        au = group[0].name
                                        link = 'https://vk.com/public{}'.format(abs(message.fwd_messages[0].from_id))
                                else:
                                    for i in range(len(message.fwd_messages)):
                                        if message.fwd_messages[i].from_id == abs(message.fwd_messages[i].from_id):
                                            user = await bp.api.users.get(message.fwd_messages[i].from_id)
                                            qu.append(user[0].first_name + ' ' + user[0].last_name + ': ' + message.fwd_messages[i].text)
                                        else:
                                            group = await bp.api.groups.get_by_id(abs(message.fwd_messages[i].from_id))
                                            qu.append(group[0].name + ': ' + message.fwd_messages[i].text)
                                    au = (await bp.api.messages.get_conversations_by_id(peer_ids=message.peer_id)).items[0].chat_settings.title

                                ans = await add_quote(None, qu, au, link, link_mes, None)
                                if (ans != False):
                                    await message.answer(ans)
                                else:
                                    await message.answer(error_mes)
                            except Exception as e:
                                if (error_up):
                                    await message.answer(prefix + e.upper())
                                else:
                                    await message.answer(e)  
                        else:
                            await message.answer(error_mes)
            except:
                if len(message.fwd_messages) != 0:
                    a = 0
                    for i in range(len(message.fwd_messages)):
                        if message.fwd_messages[i].text != '' and message.fwd_messages[i].text[0] == '!':
                            a = 1
                    if a == 0:
                        try:
                            check = []
                            qu = []
                            link = ''
                            for i in range(len(message.fwd_messages)):
                                if message.fwd_messages[i].from_id == abs(message.fwd_messages[i].from_id):
                                    user = await bp.api.users.get(message.fwd_messages[i].from_id)
                                    check.append(str(user[0].first_name + ' ' + user[0].last_name))
                                else:
                                    group = await bp.api.groups.get_by_id(abs(message.fwd_messages[i].from_id))
                                    check.append(str(group[0].name))
                            if (check.count(check[0]) == len(check)):
                                if message.fwd_messages[0].from_id == abs(message.fwd_messages[0].from_id):
                                    user = await bp.api.users.get(message.fwd_messages[0].from_id)
                                    for i in range(len(message.fwd_messages)):
                                        qu.append(message.fwd_messages[i].text)
                                    au = user[0].first_name + ' ' + user[0].last_name
                                    link = 'https://vk.com/id{}'.format(message.fwd_messages[0].from_id)
                                else:
                                    group = await bp.api.groups.get_by_id(abs(message.fwd_messages[0].from_id))
                                    for i in range(len(message.fwd_messages)):
                                        qu.append(message.fwd_messages[i].text)
                                    au = group[0].name
                                    link = 'https://vk.com/public{}'.format(abs(message.fwd_messages[0].from_id))
                            else:
                                for i in range(len(message.fwd_messages)):
                                    if message.fwd_messages[i].from_id == abs(message.fwd_messages[i].from_id):
                                        user = await bp.api.users.get(message.fwd_messages[i].from_id)
                                        qu.append(user[0].first_name + ' ' + user[0].last_name + ': ' + message.fwd_messages[i].text)
                                    else:
                                        group = await bp.api.groups.get_by_id(abs(message.fwd_messages[i].from_id))
                                        qu.append(group[0].name + ': ' + message.fwd_messages[i].text)
                                au = (await bp.api.messages.get_conversations_by_id(peer_ids=message.peer_id)).items[0].chat_settings.title

                            ans = await add_quote(None, qu, au, link, link_mes, None)
                            if (ans != False):
                                await message.answer(ans)
                            else:
                                await message.answer(error_mes)
                        except Exception as e:
                            if (error_up):
                                await message.answer(prefix + e.upper())
                            else:
                                await message.answer(e)  
                    else:
                        await message.answer(error_mes)