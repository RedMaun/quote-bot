from vkbottle.bot import Blueprint, Message
import sys, os, pkgutil
from classes.abstract_command import AbstractCommand

bp = Blueprint()

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/help', '/HELP', '/хелп', '/ХЕЛП'], description = 'shows commands usage')

Help = Command()

sys.path.insert(0, 'commands')
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module
sys.path.insert(0, '..')

import commands

@bp.on.message(text=Help.hdl())
async def help(m: Message):
    methods = [name for _, name, _ in pkgutil.iter_modules(['commands'])]
    help_list = []
    for i in range(len(methods)):
        try:
            help_list.append(', '.join(eval('commands.{}.Command().hdl()'.format(methods[i]))) + ' - ' + str(eval('commands.{}.Command().dsc()'.format(methods[i]))))
        except:
            pass
    await Help.ans_up('\n'.join(help_list), m)
    