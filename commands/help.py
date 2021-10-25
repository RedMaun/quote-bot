from vkbottle.bot import Blueprint, Message
from os import popen
bp = Blueprint()
from config.default_answer import *

exex = ['/help', '/HELP', '/хелп', '/ХЕЛП']

@bp.on.message(text=exex)
async def help(message: Message):
    description = [
        "Команды для админов:",
        "/admin, /ADMIN - добавить админа",
        "/del, /DEL - удалить админа",
        "/delete item, /DELETE item - удалить цитату, где item это индекс цитаты",
        "/edit index item text, /EDIT index item text - редактировать цитату, где index это индекс цитаты, item это редактируемый элемент(qu - содержимое цитаты; au - автор; link - ссылка на автора), text это будущее значение соответствующего элемента",
        "",
        "Команды для всех:",
        "/сьлржалсч text, /СЬЛРЖАЛСЧ text, /сьлржалсч, /СЬЛРЖАЛСЧ - цитирование сообщения, либо добавление собственной цитаты, где text это текст вашей цитаты; возможно цитирование отдельного сообщения с фото и гифками, но при пересылке нескольких сообщений файлы прикрепляться не будут!",
        "/сь index, /СЬ index - выводит определенную цитату, где index это индекс цитаты",
        "/random, /ведать, /RANDOM, /ВЕДАТЬ - рандомная цитата",
        "/лист, /ЛИСТ - отображение списка админов",
        "/uptime, /UPTIME - аптайм сервера(на котором хостится бот)",
        "/time, /TIME - время на сервере(GMT +7)",
        "/neofetch, /NEOFETCH - вывод информации neofetch с сервера",
        "/mem, /MEM, /memory, /MEMORY - количество свободной оперативной памяти на сервере",
        "",
        "https://github.com/RedMaun/quote-bot"
    ]
    await message.answer('\n'.join(description))
