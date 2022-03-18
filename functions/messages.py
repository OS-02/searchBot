# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/searchBot/a-bot/functions
File Name:     messages.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/03/17
Software:      Vscode
'''

'''Messages related functions'''
from asyncio.log import logger
import json
import logging
import pickle
from functions.glue import get_config, get_es
import telethon
from functions.login import get_bot

async def format_message(msg):
    if not msg.text or msg.media:
        return None

    chat = await msg.get_chat()
    chat_name = telethon.utils.get_display_name(chat)

    send_usr = await msg.get_sender()

    doc_data = {
        "id": msg.id,
        "date": str(msg.date),
        "sender": {
            "userName": getattr(send_usr, "username", ""),
            "firstName": getattr(send_usr, "first_name", ""),
            "lastName": getattr(send_usr, "last_name", "")
        },
        "chat": chat_name,
        "chat_id": chat.id,
        "text": msg.text
    }

    return doc_data

def update_latest_msg_id(config):
    with open(config["params"]["history"]["id_path"], "r") as f:
        ids = json.load(f)

    config["params"]["history"]["min_id"] = list(ids.values())[0]

async def save_to_es(msg):
    es = get_es()

    doc_data = await format_message(msg)

    if not doc_data:
        return 

    es.index(index="telegram", document=doc_data)

    # save latest msg id
    with open("./latest_id.json", "w") as f:
        json.dump(
            {doc_data["chat_id"]: doc_data["id"]}, f
        )

    logging.info(f"Saving Successfully: {doc_data['chat']} - {doc_data['id']} - {doc_data['date']}")

async def search_with_keyword(msg):
    bot = get_bot()

    btn = telethon.Button.inline("Page-2")

    await bot.send_message(msg.chat, "aaaaa", reply_to=msg, buttons=btn)
