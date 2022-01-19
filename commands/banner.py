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
        super().__init__(handler=['/баннер', '/БАННЕР', '/реклама', '/РЕКЛАМА'],
                         description='will add a banner to quote site')


Banner = Command()


@bp.on.message(text=Banner.hdl())
async def list(m: Message, item: Optional[int] = None):
    for banner in itertools.chain.from_iterable([x['images'] for x in await unpack(m)]):
        files_list = os.listdir(config_content['banners_dir'])
        if len(files_list) < 5:
            file = os.path.join(config_content['banners_dir'], f'{len(files_list) + 1}.webp')
        else:
            file = os.path.join(
                config_content['banners_dir'],
                min([(os.stat(os.path.join(config_content['banners_dir'],filename))[stat.ST_CTIME], filename)
                    for filename in files_list], key=lambda x: tuple.__getitem__(x, 0))[1])
            os.remove(file)
        os.replace(os.path.join(config_content['pics_dir'], banner.split('/')[-1]), file)
    await Banner.ans_up(config_content['default']['ok'], m)
