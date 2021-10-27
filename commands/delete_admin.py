from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from typing import Optional
import json

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/del <item>', '/DEL <item>', '/del', '/DEL'], description = 'delete one of the current admins')

Del = Command()

@bp.on.message(text=Del.hdl())
async def ddel(m: Message, item: Optional[str] = None):
    data = config_load(config)
    admins = data["admins"]
    super_admin = data["super_admin"]
    default = data["default"]
    if (m.from_id in admins): 
        try:
            if (item != None):
                if (item[:3] == '[id'):
                    item = int(item.replace(item[:3], '')[:9])
                    user = await bp.api.users.get(item)
                    name = user[0].first_name + ' ' + user[0].last_name
                elif (item[:5] == '[club'):
                    item = -(int(item.replace(item[:5], '')[:9]))
                    user = await bp.api.groups.get_by_id(abs(item))
                    name = user[0].name
                
                if (not(item in admins)):
                    await Del.ans_up(str(name + ' ' + default["not_admin"]), m)
                elif (super_admin == item):
                    await Del.ans_up('Удалить главного админа(раввина) нельзя', m)
                else:
                    admins.pop(admins.index(item))
                    with open(config, 'w') as file:
                        json.dump(data, file)
                    await Del.ans_up(name + ' более не является оракулом', m)

            elif (m.reply_message):
                if (m.reply_message.from_id == abs(m.reply_message.from_id)):
                    item = m.reply_message.from_id
                    user = await bp.api.users.get(item)
                    name = user[0].first_name + ' ' + user[0].last_name
                else:
                    item = m.reply_message.from_id
                    user = await bp.api.groups.get_by_id(abs(item))
                    name = user[0].name

                if (not(item in admins)):
                    await Del.ans_up(str(name + ' ' + default["not_admin"]), m)
                elif (super_admin == item):
                    await Del.ans_up('Удалить главного админа(раввина) нельзя', m)
                else:
                    admins.pop(admins.index(item))
                    with open(config, 'w') as file:
                        json.dump(data, file)
                    await Del.ans_up(name + ' более не является оракулом', m)

        except Exception as e:
            await Del.ans_up(e, m)
    else:
        await Del.ans_up(default["not_admin"], m)
    


