from config.debug_token import token
from vkbottle.bot import Bot
from vkbottle import load_blueprints_from_package

bot = Bot(token)

for bp in load_blueprints_from_package("commands"):
    bp.load(bot)
 
bot.run_forever()
    