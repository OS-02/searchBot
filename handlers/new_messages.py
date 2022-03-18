import logging
from math import ceil
import os
from functions.login import get_bot
from functions.messages import save_to_es, search_with_keyword



async def new_message_handler(event):    
    # print("#"*35)
    # print(event)
    # print("-"*45)
    # print(event.media)
    # print("#"*35)

    bot = get_bot()

    message = event.message
    
    if message.text.startswith("/start"):
        await message.reply("System all Good!")
    elif message.text.startswith("/search"):
        # Main search method
        await search_with_keyword(msg=message)
    else:
        if message.is_group:
            # save into es
            await save_to_es(msg=message)
