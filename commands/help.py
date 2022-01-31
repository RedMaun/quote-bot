from vkbottle.bot import Blueprint, Message
import sys, os, pkgutil
from classes.abstract_command import AbstractCommand
from typing import Optional

bp = Blueprint()

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/help', '/хелп', '/HELP', '/ХЕЛП'], description = 'shows commands usage')

Help = Command()

@bp.on.message(text=Help.hdl())
async def help(m: Message):
    await Help.ans_up('https://vk.com/@slrzhalsch-manual', m)
    

    

# class Command(AbstractCommand):
#     def __init__(self):
#         super().__init__(handler = ['/help', '/help <item>', '/HELP', '/HELP <item>', '/хелп', '/хелп <item>', '/ХЕЛП', '/ХЕЛП <item>'], description = 'shows commands usage')

# Help = Command()

# sys.path.insert(0, 'commands')
# for module in os.listdir(os.path.dirname(__file__)):
#     if module == '__init__.py' or module[-3:] != '.py':
#         continue
#     __import__(module[:-3], locals(), globals())
# del module
# sys.path.insert(0, '..')

# import commands

# @bp.on.message(text=Help.hdl())
# async def help(m: Message, item: Optional[str] = None):
#     methods = [name for _, name, _ in pkgutil.iter_modules(['commands'])]
#     help_list = []
#     for i in range(len(methods)):
#         try:
#             help_list.append(', '.join(eval('commands.{}.Command().hdl()'.format(methods[i]))) + ' - ' + str(eval('commands.{}.Command().dsc()'.format(methods[i]))))
#         except:
#             try:
#                 help_list.append(', '.join(eval('commands.{}.Command1().hdl()'.format(methods[i]))) + ' - ' + str(eval('commands.{}.Command1().dsc()'.format(methods[i]))))
#                 help_list.append(', '.join(eval('commands.{}.Command2().hdl()'.format(methods[i]))) + ' - ' + str(eval('commands.{}.Command2().dsc()'.format(methods[i]))))
#             except:
#                 pass
    
#     if (item):
#         for i in help_list:
#             if item in i:
#                 await Help.ans_up(i, m)
#                 break
#     else:
#         help_list.append('-----------------------------------------------------------------------------\nGithub - https://github.com/RedMaun/quote-bot')
#         await Help.ans_up('\n\n'.join(help_list), m)

    