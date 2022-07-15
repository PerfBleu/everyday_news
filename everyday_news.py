__version__ = '0.1.0'
import os
#from PIL import Image, ImageFont, ImageDraw
#from hoshino import util, R
from hoshino import Service
import requests as req
import json

sv = Service('everydayNews', visible= True, enable_on_default= True, bundle='everydayNews', help_='''
每日简报
'''.strip())
path = os.path.dirname(__file__)
def getPicUrl():
    getObject = req.get('http://118.31.18.68:8080/news/api/news-file/get')
    if getObject.status_code != 200:
        sv.logger.warning('URL获取失败')
        return()
    else:
        sv.logger.info('图片URL获取成功')
    return(json.loads(getObject.text)['result'][0])
def getImg():
    getObject = req.get(
        #headers={'Referer':'safe.soyiji.com'},
        url=getPicUrl()
    )
    if getObject.status_code != 200:
        sv.logger.warning(f'图片获取失败{getObject.status_code}')
        return()
    else:
        sv.logger.info('图片获取成功')
    with open(os.path.join(path, "tmp.jpg"),'wb') as image:
        image.write(getObject.content)


@sv.on_fullmatch(('每日简报','报哥','每日新闻','今日新闻','今日简报'))
async def news(bot,ev):
    getImg()
    tmppath = os.path.join(path, "tmp.jpg")
    await bot.send(ev, f"[CQ:image,file=file:///{tmppath}]", at_sender=True)

@sv.scheduled_job('cron', hour = '9' ,minute='30')
async def news_scheduled():
    getImg()
    tmppath = os.path.join(path, "tmp.jpg")
    await sv.broadcast(f"[CQ:image,file=file:///{tmppath}]",'auto_send_news_message', 2)