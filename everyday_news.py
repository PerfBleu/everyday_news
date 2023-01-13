__version__ = '0.2.0'
import os
from hoshino import Service
from hoshino import aiorequests as req
from hoshino.util import pic2b64
from PIL import Image
from io import BytesIO
import json

sv = Service('everydayNews', visible= True, enable_on_default= True, bundle='everydayNews', help_='''
每日简报
'''.strip())
path = os.path.dirname(__file__)

async def getPicUrl():
    # api修复
    getObject = await req.get('http://118.31.18.68:8080/news/api/news-file/get')
    if getObject.status_code != 200:
        sv.logger.warning('URL获取失败')
        return()
    else:
        sv.logger.info('图片URL获取成功')
    return(json.loads(await getObject.text)['result']['data'][0])

async def getImg():
    getObject = await req.get(
        # headers={'Referer':'safe.soyiji.com'},
        url=await getPicUrl()
    )
    if getObject.status_code != 200:
        sv.logger.warning(f'图片获取失败{getObject.status_code}')
        return()
    else:
        sv.logger.info('图片获取成功')
    # with open(os.path.join(path, "tmp.jpg"),'wb') as image:
    #     image.write(await getObject.content)
    image = Image.open(BytesIO(await getObject.content))
    return f'[CQ:image,file={pic2b64(image)}]'


@sv.on_fullmatch(('每日简报','报哥','每日新闻','今日新闻','今日简报'))
async def news(bot,ev):
    img = await getImg()
    # tmppath = os.path.join(path, "tmp.jpg")
    await bot.send(ev, img, at_sender=True)

@sv.scheduled_job('cron', hour = '9')
async def news_scheduled():
    img = await getImg()
    # tmppath = os.path.join(path, "tmp.jpg")
    await sv.broadcast(img,'auto_send_news_message', 2)
