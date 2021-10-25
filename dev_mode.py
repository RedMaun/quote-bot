from config.token import token
from typing import Optional
import sys
from os import system
from config.super_admin import super_admin
from vkbottle.bot import Bot, Message
from config.default_answer import *
from config.peer_id import peer_id
sys.path.insert(0, './commands')
import asyncio

bot = Bot(token)

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('commands') if isfile(join('commands', f))]

b = []

sys.path.insert(0, '..')
for g in range(len(onlyfiles)):
    f = open('commands/' + onlyfiles[g], 'r')
    Lines = f.readlines()
    for line in Lines:
        if 'exex' in line and '[' in line:
            s = line.replace('\n', '')
            start = '['
            end = ']'
            a = (s[s.find(start)+len(start):s.rfind(end)]).replace('\'', '').split(', ')
            for i in range(len(a)):
                b.append(a[i])
    f.close()

async def start():
    if (peer_id != None or peer_id != ''):
        await bot.api.messages.send(peer_id=peer_id, message='Включен режим отладки', random_id=0)
        f = open('config/peer_id.py', 'w')
        f.write("peer_id = ''")
        f.close()

@bot.on.message(text=b)
async def debugging(message: Message):
    await message.answer('В настоящее время бот находится в режиме отладки. \n Вы можете написать [id{}|разработчику]'.format(super_admin[0]))

@bot.on.message(text=['/run', '/RUN'])
async def run(message: Message):
    if str(message.from_id) in super_admin:
        if (message.text == '/run'):
            await message.answer('Загрузка...')
            f = open('config/peer_id.py', 'w')
            f.write('peer_id = {}'.format(message.peer_id))
            f.close()
            system('systemctl restart bot')
            system('systemctl stop debug')
            system('systemctl stop dev')
        else:
            await message.answer(prefix + 'ВКЛЮЧАЮСЬ')
            f = open('config/peer_id.py', 'w')
            f.write('peer_id = {}'.format(message.peer_id))
            f.close()
            system('systemctl restart bot')
            system('systemctl stop debug')
            system('systemctl stop dev')
    else:
        if (message.text == '/stop'):
            await message.answer(not_admin)
        else:
            await message.answer(prefix + not_admin.upper())

bot.loop_wrapper.add_task(start())
bot.run_forever()