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
import prettytable
import math

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
    config = get_config()

    doc_data = await format_message(msg)

    if not doc_data:
        return 

    es.index(index=config["es"]["index"], document=doc_data)

    # save latest msg id
    with open("./latest_id.json", "w") as f:
        json.dump(
            {doc_data["chat_id"]: doc_data["id"]}, f
        )

    logging.info(f"Saving Successfully: {doc_data['chat']} - {doc_data['id']} - {doc_data['date']}")

async def search_with_keyword(msg):
    bot = get_bot()
    es = get_es()
    config = get_config()

    query = {
        "match": {
            "text": "".join(msg.text.split(' ')[1:])
        }
    }


    res = es.search(index=config["es"]["index"], from_=0, size=config["params"]["search"]["step"], query=query)

    # no hit
    if res.body["hits"]["total"]["value"] == 0:
        await bot.send_message(msg.chat, f"👋🏼No match for {''.join(msg.text.split(' ')[1:])}", reply_to=msg)
        return 
    # print(res.body)

    pretty_res = prettified_res(res=res, keyword="".join(msg.text.split(' ')[1:]))

    # print(pretty_res)

    btn = telethon.Button.inline("Page-2")

    await bot.send_message(msg.chat, pretty_res, reply_to=msg, buttons=btn)


    # btn = telethon.Button.inline("Page-2")

    # await bot.send_message(msg.chat, "aaaaa", reply_to=msg, buttons=btn)


def prettified_res(res, keyword, page=1):
    config = get_config()
    table = prettytable.PrettyTable()

    table.field_names = [
        "⏰Date",
        "👤Sender",
        "🔊Text",
        # "Chat"
    ]

    table.align["Text"] = "l"

    # calculate total page: total_hits/step
    total_page = math.ceil(res.body["hits"]["total"]["value"]/config["params"]["search"]["step"])

    # table.add_row(("2022-03-18", "aSigma", "哈哈哈", "111"))
    stack_msg = ""
    for row in res.body["hits"]["hits"]:
        # table.add_row((
        #     row["_source"]["date"].split(" ")[0],
        #     row["_source"]["sender"]["userName"],
        #     # row["_source"]["text"],
        #     f"[{row['_source']['text']}](https://t.me/nbb_love_tanaka/{row['_source']['id']})"
        #     # row["_source"]["chat"]
        # ))
        stack_msg += f"📆 {row['_source']['date'].split(' ')[0]}  --|--  👤 {row['_source']['sender']['userName']}\n" \
                     f"🔊 [{row['_source']['text']}](https://{config['chat']}/{row['_source']['id']})\n" \
                     f"{'-'*50}\n\n"

    prety_res = f"📝Total page: {total_page}\n" \
          f"👀Page-{page} for keyword: **{keyword}**\n\n" \
          f"{stack_msg}" 

    return prety_res
