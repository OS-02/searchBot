# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/searchBot/a-bot/handlers
File Name:     callback_query.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/03/17
Software:      Vscode
'''


'''CallbackQueryHandler aka inline button handler'''
import re
import telethon
from functions.login import get_bot
from functions.glue import get_config
from functions.glue import get_es
from functions.messages import prettified_res

async def callback_query_handler(event):
    # print(event)
    # print(1)

    # page = int(str(event.data, encoding="utf-8").split("-")[-1])
    # btn = telethon.Button.inline(f"Page-{str(page+1)}")

    # bot = get_bot()

    # print(await event.get_message())

    # print(111)

    bot = get_bot()
    config = get_config()
    es = get_es()
    step = config["params"]["search"]["step"]

    request_page = int(str(event.data, encoding="utf-8").split("-")[-1])
    msg = await event.get_message()
    total_page = int(re.findall(r"page: (.*)", msg.message.split("\n")[0])[0])
    keyword = re.findall(r"keyword: (.*)", msg.message.split("\n")[1])[0]

    query = {
        "match": {
            "text": keyword
        }
    }
    
    res = es.search(index=config["es"]["index"], from_=step*(request_page-1), size=config["params"]["search"]["step"], query=query)
    pretty_res = prettified_res(res=res, keyword=keyword, page=request_page)
    if request_page < total_page:
        btn = telethon.Button.inline(f"Page-{str(request_page+1)}")
        await bot.send_message(event.chat, pretty_res, buttons=btn)
    else:
        await bot.send_message(event.chat, pretty_res)
        await bot.send_message(event.chat, f"🫕That's all for {keyword} for now~")
