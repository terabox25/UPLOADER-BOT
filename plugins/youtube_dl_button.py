import os
import json
import math
import time
import shutil
import asyncio
from PIL import Image
from config import Config
from datetime import datetime
from database.access import clinton
from translation import Translation
from plugins.custom_thumbnail import *
from pyrogram.types import InputMediaPhoto
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes

async def youtube_dl_call_back(bot, update):
    try:
        cb_data = update.data
        tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
        save_ytdl_json_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".json"
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except Exception:
        # Delete message or callback query message if available
        if update.message:
            await update.message.delete(True)
        elif update.callback_query and update.callback_query.message:
            await update.callback_query.message.delete(True)
        return

    # Handle reply_to_message properly, since it might be in either message or callback query
    if update.message:
        reply_to_message = update.message.reply_to_message
    elif update.callback_query:
        reply_to_message = update.callback_query.message.reply_to_message
    else:
        return  # No valid reply-to message

    youtube_dl_url = reply_to_message.text if reply_to_message else None
    custom_file_name = str(response_json.get("title"))[:50] + "_" + youtube_dl_format

    # Handle the rest of the logic
    youtube_dl_username = None
    youtube_dl_password = None
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        elif len(url_parts) == 4:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
    else:
        for entity in reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]

    # Continue with downloading and uploading logic
    await update.message.edit(text=Translation.DOWNLOAD_START)
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
    
    # Process the file download and handling logic...
    

#=================================

async def clendir(directory):

    try:
        os.remove(directory)
    except:
        pass
    try:
        shutil.rmtree(directory)
    except:
        pass

#=================================
