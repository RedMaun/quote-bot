from wand.image import Image
from wand.drawing import Drawing 
from vkbottle.bot import Blueprint, Message
from vkbottle import PhotoMessageUploader
from typing import Optional

bp = Blueprint()

handler = ['/жириновский <item>', '/жирик <item>']

async def suggested(txt):
    with open('pics/zhir.jpeg', 'rb') as f:
        pattern = f.read()
    b = ['есть идея', 'мб', 'может быть', 'предложил', 'предлагаю', 'а может', 'может', 'давайте', 'давай', '?']
    txt = txt.lower()
    for x in b: txt = txt.replace(x, '')
    with Image(blob=pattern) as img:
        with Image(width=560, height=360) as img2:
            with Drawing() as draw: 
                draw.font = 'NotoSans-Regular'
                draw.font_size = 44
                n = 22
                txt = txt.split()
                text = ['']
                g = 0
                for i in range(len(txt)):
                    if (len(text[g] + txt[i]) > 22):
                        g += 1
                        text.append('')
                    
                    text[g] += txt[i] + ' '
                    
                for i in range(0, len(text)):
                    draw.text(0, 45*(i+1), text[i]) 

                draw(img2) 
            img.composite(image=img2, left=50, top=630)
        img.merge_layers('flatten')
        img.format = 'jpeg'
        img_bytes = img.make_blob()

        photo_uploader = PhotoMessageUploader(bp.api, generate_attachment_strings=True)

        return await photo_uploader.upload(img_bytes)

@bp.on.message(text=handler)
async def zhir(m: Message, item: Optional[str] = None):
    img = await suggested(item)
    await m.answer(attachment=img)
    

    

    

    
    

    