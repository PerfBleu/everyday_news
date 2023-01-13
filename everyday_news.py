__version__ = '0.2.0'
import os
from hoshino import Service, get_self_ids, priv
from hoshino import aiorequests as req
from hoshino.util import pic2b64
from nonebot import get_bot
from PIL import Image
from io import BytesIO
import json
import asyncio

from .config import get_group_config_byindex, set_group_config_byindex

sv = Service('everydayNews', visible= True, enable_on_default= True, bundle='everydayNews', help_='''
每日简报
'''.strip())
path = os.path.dirname(__file__)

async def getPicUrl():
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

    image = Image.open(BytesIO(await getObject.content))
    return f'[CQ:image,file={pic2b64(image)}]'


@sv.on_fullmatch(('每日简报','报哥','每日新闻','今日新闻','今日简报'))
async def news(bot,ev):
    img = await getImg()
    # tmppath = os.path.join(path, "tmp.jpg")
    await bot.send(ev, img, at_sender=True)

# @sv.scheduled_job('cron', hour = '9')
# async def news_scheduled():
#     img = await getImg()
#     # tmppath = os.path.join(path, "tmp.jpg")
#     await sv.broadcast(img,'auto_send_news_message', 2)

@sv.scheduled_job('cron', hour = '9')
async def news_scheduled():
    img = await getImg()
    bot = get_bot()
    sids = get_self_ids()
    for sid in sids:
        for gid in await bot.get_group_list(self_id = sid):
            if get_group_config_byindex(gid):
                bot.send_group_msg(self_id = sid, group_id = gid, message = img)
                asyncio.sleep(1000)

@sv.on_fullmatch(('停止简报推送','禁用简报推送'))
async def news_off(bot,ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev,"权限不足")
    set_group_config_byindex(gid=ev.group_id, index=0, setting=False)
    await bot.send(ev, '本群简报推送已禁用', at_sender=True)

@sv.on_fullmatch(('启用简报推送','开启简报推送'))
async def news_on(bot,ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev,"权限不足")
    set_group_config_byindex(gid=ev.group_id, index=0, setting=True)
    await bot.send(ev, '本群简报推送已启用', at_sender=True)