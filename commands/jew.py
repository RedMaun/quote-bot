from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from typing import Optional

bp = Blueprint()

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/еврей <k> <item>', '/ЕВРЕЙ <k> <item>', '/еврей <item>', '/ЕВРЕЙ <item>'], description = 'jewificator v1.756')

Jew = Command()

@bp.on.message(text = Jew.hdl())
async def jewificator(m: Message, k: Optional[str] = None, item: Optional[int] = None):
    try:
        if k == None:
            answer = "("*3 + item + ")"*3
            await Jew.ans_up(answer, m)
        elif int(k) < 100 and int(k) > 0:
            k = int(k)
            if isinstance(k, int):
                answer = "("*k + item + ")"*k
                await Jew.ans_up(answer, m)
            else:
                await Jew.ans_up('errors', m)
        else:
            await Jew.ans_up('must be int in range (0, 100)', m)
    except Exception as e:
        await Jew.ans_up(e, m)
    