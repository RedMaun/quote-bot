from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
import json
bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/list', '/LIST', '/лист', '/ЛИСТ'], description = 'display admins list')

List = Command()

@bp.on.message(text = List.hdl())
async def list(m: Message):
    data = config_load(config)
    admins = data["admins"]
    default = data["default"]
    try:
        list_names = []
        for i in range(len(admins)):
            if (abs(admins[i]) == admins[i]):
                user = await bp.api.users.get(admins[i])
                name = user[0].first_name + ' ' + user[0].last_name
            else:
                user = await bp.api.groups.get_by_id(abs(admins[i]))
                name = user[0].name
            list_names.append(str(name))
        await List.ans_up('\n'.join(list_names), m)
    except Exception as e:
        await List.ans_up(e, m)
