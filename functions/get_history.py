# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/searchBot/a-bot/functions
File Name:     get_history.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/03/17
Software:      Vscode
'''


'''Get chat history as a real person'''

from telethon import TelegramClient
from functions.glue import get_config
from functions.messages import format_message, save_to_es, update_latest_msg_id
from tqdm.asyncio import tqdm

async def load_history():
    config = get_config()

    if config["params"]["history"]["id_path"]:
        update_latest_msg_id(config)

    async with TelegramClient("chaos", api_id=config["bot"]["api_id"], api_hash=config["bot"]["api_hash"], proxy=config['proxy']) as client:
        async for msg in tqdm(client.iter_messages(config["chat"], limit=config["params"]["history"]["limit"], min_id=config["params"]["history"]["min_id"])):
            # print("-"*25)
            # print(await format_message(msg))
            # print("-"*25)

            await save_to_es(msg=msg)
