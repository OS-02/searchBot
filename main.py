# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/telePicCutBot
File Name:     main.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/02/27
Software:      Vscode
'''

'''Main Entrence of the whole Bot'''
import asyncio
from audioop import lin2adpcm
from distutils.command.clean import clean
import logging
from re import T
import telethon
import yaml

# Set parameters
from argparse import ArgumentParser
from telethon import events, TelegramClient
from functions.glue import get_config, init_es, read_config, set_logger

from functions.login import get_bot, login
from handlers.new_messages import new_message_handler
from handlers.callback_query import callback_query_handler
from functions.get_history import load_history
import re



parser = ArgumentParser()

parser.add_argument("--config", "-c", default="search-bot/config.yaml", help="Configeration file")

args = parser.parse_args()

async def main():
    # Read the configs
    print("Reading Configurations...")
    read_config(args.config)
    config = get_config()

    # Set logger
    set_logger(config=config)

    # Set mode
    if config["params"]["debug"]:
        loop = asyncio.get_event_loop()
        loop.set_debug(enabled=True)

    # init es
    logging.info("Setting elastic search")
    init_es(config)

    # get history until config['oldest'], need to login as Chaos
    await load_history()

    # login the bot account
    login(config=config)
    bot = get_bot()
    logging.info("Logged in as a bot")

    # add handler: listening all new messages from given chats by config file
    logging.info("Adding New Message handler")
    logging.info("Adding Callback Query handler")
    if config["private"]["enable"]:
        bot.add_event_handler(new_message_handler, event=events.NewMessage(from_users=config["private"]["auth_user"]))
        bot.add_event_handler(callback_query_handler, event=events.CallbackQuery(data=re.compile("Page-")))
    else:
        bot.add_event_handler(new_message_handler, event=events.NewMessage())
        bot.add_event_handler(callback_query_handler, event=events.CallbackQuery(data="Page-*"))

    # start the bot
    logging.info("Bot Started!")
    await bot.start(bot_token=config["bot"]["bot_token"])

    # run forever
    await bot.run_until_disconnected()


if __name__ == '__main__':   
    asyncio.run(main())
