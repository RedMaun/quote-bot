import itertools

from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from typing import Optional
from commands.quote import unpack, config_content
import os
import stat

bp = Blueprint()


class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler=['/баннер <item>', '/БАННЕР <item>', '/реклама <item>', '/РЕКЛАМА <item>'],
                         description='will add a banner to quote site')


Banner = Command()


@bp.on.message(text=Banner.hdl())
async def list(m: Message, item: Optional[int] = None):
    if item == None:
        for banner in itertools.chain.from_iterable([x['images'] for x in await unpack(m)]):
            files_list = os.listdir(config_content['banners_dir'])
            if len(files_list) < 4:
                file = os.path.join(config_content['banners_dir'], f'{len(files_list) + 1}.webp')
            else:
                file = os.path.join(
                    config_content['banners_dir'],
                    min([(os.stat(os.path.join(config_content['banners_dir'],filename))[stat.ST_CTIME], filename)
                        for filename in files_list], key=lambda x: x[0])[1])
                os.remove(file)
            os.replace(os.path.join(config_content['pics_dir'], banner.split('/')[-1]), file)
        await Banner.ans_up(config_content['default']['ok'], m)
    else:
        try:
            item = int(item)
            if item in range(1, 6):
                for banner in itertools.chain.from_iterable([x['images'] for x in await unpack(m)]):
                    files_list = os.listdir(config_content['banners_dir'])
                    file = os.path.join(config_content['banners_dir'], str(item) + '.webp')
                    if str(item) + '.webp' in files_list:
                        os.remove(file)
                    os.replace(os.path.join(config_content['pics_dir'], banner.split('/')[-1]), file)
                    await Banner.ans_up(config_content['default']['ok'], m)
                    break
        except Exception as e:
            await Banner.ans_up(e, m)
