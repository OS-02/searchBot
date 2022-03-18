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
import telethon
from functions.login import get_bot

async def callback_query_handler(event):
    print(event)

    page = int(str(event.data, encoding="utf-8").split("-")[-1])
    btn = telethon.Button.inline(f"Page-{str(page+1)}")

    bot = get_bot()

    await bot.send_message(event.chat, "这是另一页的搜索结果", buttons=btn)

    print(111)