__version__ = '0.1.0'
import os
#from PIL import Image, ImageFont, ImageDraw
#from hoshino import util, R
from hoshino import Service
import requests as req
import json

sv = Service('everydayNews', visible= True, enable_on_default= True, bundle='everydayNews', help_='''
每日简报，请发送“每日简报、报哥或每日新闻”
'''.strip())
path = os.path.dirname(__file__)
def getPicUrl():
    getObject = req.get('http://api.soyiji.com//news_jpg')
    if getObject.status_code != 200:
        sv.logger.warning('URL获取失败')
        return()
    else:
        sv.logger.info('图片URL获取成功')
    return(json.loads(getObject.text)['url'])

def getImg():
    getObject = req.get(
        headers={'Referer':'safe.soyiji.com'},
        url=getPicUrl()
    )
    if getObject.status_code != 200:
        sv.logger.warning('图片获取失败')
        return()
    else:
        sv.logger.info('图片获取成功')
    with open(os.path.join(path, "tmp.jpg"),'wb') as image:
        image.write(getObject.content)


@sv.on_fullmatch(('每日简报','报哥','每日新闻'))
async def news(bot,ev):
    getImg()
    tmppath = os.path.join(path, "tmp.jpg")
    await bot.send(ev, f"[CQ:image,file=file:///{tmppath}]", at_sender=True)

@sv.scheduled_job('cron', hour = '9')
async def news_scheduled(bot,ev):
    getImg()
    tmppath = os.path.join(path, "tmp.jpg")
    await bot.send(ev, f"[CQ:image,file=file:///{tmppath}]")
