import random

import asyncio

from datetime import datetime

from ..core.managers import edit_or_reply

from . import catub, hmention

plugin_category = "tools"

import re

import time

from platform import python_version

from telethon import version

from telethon.errors.rpcerrorlist import (

    MediaEmptyError,

    WebpageCurlFailedError,

    WebpageMediaEmptyError,

)

from telethon.events import CallbackQuery

import asyncio

from datetime import datetime

from userbot import catub

from ..core.managers import edit_or_reply

from ..Config import Config

from ..core.managers import edit_or_reply

from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time

from ..helpers.utils import reply_id

from ..sql_helper.globals import gvarstatus

from . import StartTime, catub, catversion, mention

plugin_category = "utils"

@catub.cat_cmd(

    pattern="بوت$",

    command=("بوت", plugin_category),

    info={

        "header": "للتأكد من حالة عمل البوت",

        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",

        "usage": [

            "{tr}alive",

        ],

    },

)

async def amireallyalive(event):

    "A kind of showing bot details"

    reply_to_id = await reply_id(event)

    uptime = await get_readable_time((time.time() - StartTime))

    _, check_sgnirts = check_data_base_heal_th()

    EMOJI = gvarstatus("ALIVE_EMOJI") or "   ┃‣ 🍒 "

    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "⇝𝗪َ𝗘𝗟َِ𝗖𝗢𝗠َِ𝙀َِ 𝗧𝗢 𓆩𝐏𝐑𝐎𓆪⇜"

    CAT_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/47b6a423bab8cbc66e186.jpg"
    
    flag = event.pattern_match.group(1)

    start = datetime.now()
    
    catevent = await edit_or_reply(event, "`!....`")
        await asyncio.sleep(0.3)
        await catevent.edit("`..!..`")
        await asyncio.sleep(0.3)
        await catevent.edit("`....!`")
        end = datetime.now()
        ms = (end - start).microseconds / 1000

    
    if CAT_IMG:

        CAT = [x for x in CAT_IMG.split()]

        A_IMG = list(CAT)

        PIC = random.choice(A_IMG)

        cat_caption = f"**{ALIVE_TEXT}**\n\n"

        

        cat_caption += f"            ┏━━━━━✦❘༻༺❘✦━━━━━┓\n"

        cat_caption += f"**{EMOJI} المنشئ ↞ :** {mention}\n"

        cat_caption += f"**{EMOJI} المؤقت ↞ :** `{uptime}\n`"

        cat_caption += f"**{EMOJI} اصدار تليثون ↞ :** `{version.__version__}\n`"

        cat_caption += f"**{EMOJI} اصدار برو ↞ :** `{catversion}`\n"

        cat_caption += f"**{EMOJI} اصدار بايثون ↞ :** `{python_version()}\n`"

        cat_caption += f"**{EMOJI} قاعدة البيانات ↞ :** تعمل بنجاح. \n"

        cat_caption += f"            ┗━━━━━✦❘༻༺❘✦━━━━━┛\n"

        cat_caption += f"            ┏━━━━━✦❘༻༺❘✦━━━━━┓\n"

        cat_caption += f"**{EMOJI} البينغ ↞ :** `{ms}ms`\n"

        cat_caption += f"            ┗━━━━━✦❘༻༺❘✦━━━━━┛\n"

        cat_caption += f" ‣ البوت برو يعمل بنجاح✔، **[قناة السورس]**(t.me/moussa_pro)🧸\n"

        try:

            await event.client.send_file(

                event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id

            )

            await event.delete()

        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):

            return await edit_or_reply(

                event,

                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can t get media from this link :-**__ `{PIC}`",

            )

    else:

        await edit_or_reply(

            event,

            f"**{ALIVE_TEXT}**\n\n"

            f"**{EMOJI} المنشئ ↞ : {mention}**\n"

            f"**{EMOJI} المؤقت ↞ :** `{uptime}\n`"

            f"**{EMOJI} اصدار تليثون ↞ :** `{version.__version__}\n`"

            f"**{EMOJI} اصدار برو ↞ :** `{catversion}`\n"

            f"**{EMOJI} اصدار بايثون ↞ :** `{python_version()}\n`"

            f"**{EMOJI} قاعدة البيانات ↞ : `{check_sgnirts}`\n",

        )

@catub.cat_cmd(

    pattern="برو$",

    command=("برو", plugin_category),

    info={

        "header": "لعرض معلومات حول البوت",

        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",

        "usage": [

            "{tr}alive",

        ],

    },

)

async def amireallyalive(event):

    "A kind of showing bot details by your inline bot"

    reply_to_id = await reply_id(event)

    EMOJI = gvarstatus("ALIVE_EMOJI") or "🍒"

    cat_caption = f"**[𝐖𝐄𝐋𝐂𝐎𝐌𝐄  𝐓𝐎 ℙℝ𝕆 𝕌𝕊𝔼ℝ 𝔹𝕆𝕋⇜\n"

    cat_caption += f"**{EMOJI} اصدار تليثون ↞ :** `{version.__version__}\n`"

    cat_caption += f"**{EMOJI} اصدار برو ↞ :** `{catversion}`\n"

    cat_caption += f"**{EMOJI} اصدار بايثون ↞ :** `{python_version()}\n`"

    cat_caption += f"**{EMOJI} المنشئ ↞ :** {mention}\n"

    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)

    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)

    await event.delete()

@catub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))

async def on_plug_in_callback_query_handler(event):

    statstext = await catalive(StartTime)

    await event.answer(statstext, cache_time=0, alert=True)

