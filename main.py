import json
from vkbottle.bot import Bot
from vkbottle import load_blueprints_from_package

config = 'config.json'

with open(config, 'r') as f:
    data = json.load(f)

token = data["token"]

bot = Bot(token)

for bp in load_blueprints_from_package("commands"):
    bp.load(bot)

bot.run_forever()
    
