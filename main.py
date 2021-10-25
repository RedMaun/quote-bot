from config.token import token
from vkbottle.bot import Bot
from vkbottle import load_blueprints_from_package
from config.peer_id import peer_id

bot = Bot(token)

for bp in load_blueprints_from_package("commands"):
    bp.load(bot)

async def start():
    if (peer_id != None or peer_id != ''):
        await bot.api.messages.send(peer_id=peer_id, message='Бот включен', random_id=0)
        f = open('config/peer_id.py', 'w')
        f.write("peer_id = ''")
        f.close()

bot.loop_wrapper.add_task(start())
bot.run_forever()
    
