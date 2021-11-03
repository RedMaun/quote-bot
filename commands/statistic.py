from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from db.connect import collection
from vkbottle import PhotoMessageUploader
from typing import Optional
import pygal
import cairosvg
from pygal import Config
import datetime
from random import randint as rand
from iteration_utilities import deepflatten

bp = Blueprint()

config = 'config.json'

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/статистика <n> <item>', '/статистика <n>', '/статистика', '/СТАТИСТИКА <n> <item>', '/СТАТИСТИКА <n>', '/СТАТИСТИКА'], description = 'statistics, <n> = 0, 1, 2 - different graphs')

Stat = Command()

@bp.on.message(text = Stat.hdl())
async def sear(m: Message, n: Optional[int] = None, item: Optional[int] = None):
    photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)
    # try:
    if (n != None and int(n) == 1):
        cursor = collection.find({})
        authors = []
        for i in cursor:
            if ("au" in i):
                authors.append(i["au"])
        orig = list(set(authors))
        line_chart = pygal.HorizontalBar()
        line_chart.title = 'Количество цитат от определенного автора'
        b = []
        for i in range(len(orig)):
            b.append([authors.count(orig[i]), orig[i]])
        b = sorted(b, reverse=True)
        for i in b:
            line_chart.add(i[1], i[0])
        name = str(rand(100000, 999999))
        cairosvg.svg2png(bytestring=line_chart.render(is_unicode=True).encode('utf8'), write_to='/tmp/{}.png'.format(name))
        graph = await photo_uploader.upload('/tmp/{}.png'.format(name))
        await Stat.ans_up('', m, graph)
    elif (n != None and int(n) == 2):
        qu = ''
        cursor = collection.find({})
        for i in cursor:
            if ("qu" in i):
                if (isinstance(i["qu"], dict) or isinstance(i["qu"], list) and isinstance(list(deepflatten(i["qu"], ignore=dict))[0], dict)):
                    c = list(deepflatten(i["qu"], ignore=dict))
                    for g in c:
                        qu += ' '.join(g["text"].split('\n')).lower() + ' '
                elif (isinstance(i["qu"], list)):
                    for g in i["qu"]:
                        qu += ' '.join(g.split('\n')).lower() + ' '
                elif (isinstance(i["qu"], str)):
                    qu += ' '.join(i["qu"].split('\n')).lower() + ' '
        
        qu = qu.replace(',', '').replace('.', '').replace('!', '').replace(':', '')
        qu = qu.split(' ')
        orig = list(set(qu))
        b = []
        for i in orig:
            if qu.count(i) > 4 and len(i) > 2:
                b.append([qu.count(i), i])

        b = sorted(b, reverse=True)
        line_chart = pygal.HorizontalBar()
        line_chart.title = 'Самое популярное слово'
        for i in b:
            line_chart.add(i[1], i[0])
        name = str(rand(100000, 999999))
        cairosvg.svg2png(bytestring=line_chart.render(is_unicode=True).encode('utf8'), write_to='/tmp/{}.png'.format(name))
        graph = await photo_uploader.upload('/tmp/{}.png'.format(name))
        await Stat.ans_up('', m, graph)
        

    elif (n != None and int(n) == 0 or n == None):
        cursor = collection.find({})
        _dates = []
        for i in cursor:
            if ("da" in i):
                _dates.append(i["da"][:10])
        config = Config()
        config.show_legend = False
        config.fill = True
        config.title = 'Статистика цитат'
        config.y_title = 'Кол-во цитат'
        line_chart = pygal.Bar(config, x_label_rotation=-45)
        orig = list(set(_dates))

        dates = [datetime.datetime.strptime(ts, "%d.%m.%Y") for ts in orig]
        dates.sort()
        sorteddates = [datetime.datetime.strftime(ts, "%d.%m.%Y") for ts in dates]
        b = []
        h = []
        if (item != None):
            if (int(item) >= len(sorteddates)):
                for i in range(len(sorteddates)):
                    b.append(_dates.count(sorteddates[i]))
                    h.append(sorteddates[i])
            else:
                for i in range(len(sorteddates)-int(item), len(sorteddates)):
                    b.append(_dates.count(sorteddates[i]))
                    h.append(sorteddates[i])
        else:
            for i in range(len(sorteddates)):
                b.append(_dates.count(sorteddates[i]))
                h.append(sorteddates[i])

        line_chart.x_labels = h
        
        line_chart.add('Кол-во цитат', b)
        name = str(rand(100000, 999999))
        cairosvg.svg2png(bytestring=line_chart.render(is_unicode=True).encode('utf8'), write_to='/tmp/{}.png'.format(name))
        graph = await photo_uploader.upload('/tmp/{}.png'.format(name))
        await Stat.ans_up('', m, graph)

    # except Exception as e:
    #     await Stat.ans_up(e, m)
