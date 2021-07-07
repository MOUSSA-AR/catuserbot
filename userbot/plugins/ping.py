import asyncio

from datetime import datetime

from ..core.managers import edit_or_reply

from . import catub, hmention

plugin_category = "tools"

@catub.cat_cmd(

    pattern="بينغ( -a|$)",

    command=("بينغ", plugin_category),

    info={

        "header": "فحص سرعة البوت برو",

        "flags": {"-a": "average ping"},

        "usage": ["{tr}ping", "{tr}ping -a"],

    },

)

async def _(event):

    "فحص سرعة البوت"

    flag = event.pattern_match.group(1)

    start = datetime.now()

    if flag == " -a":

        catevent = await edit_or_reply(event, "`!....`")

        await asyncio.sleep(0.3)

        await catevent.edit("`..!..`")

        await asyncio.sleep(0.3)

        await catevent.edit("`....!`")

        end = datetime.now()

        tms = (end - start).microseconds / 1000

        ms = round((tms - 0.6) / 3, 3)

        await catevent.edit(f"**↫ البينغ هو!**\n {ms} ms ↫")

    else:

        catevent = await edit_or_reply(event, "<b><i>↫ البينغ هو!</b></i>", "html")

        end = datetime.now()

        ms = (end - start).microseconds / 1000

        await catevent.edit(

            f"<b><i>↫ البينغ هو!</b></i>\n {ms} <b><i>ms",

            parse_mode="html",

        )

@catub.cat_cmd(

    pattern="بينغ برو$",

    command=("بينغ برو", plugin_category),

    info={"header": "لفحص سرعة البينغ", "usage": "{tr}fping"},

)

async def _(event):

    "لفحص البينغ "

    start = datetime.now()

    animation_interval = 0.3

    animation_ttl = range(26)

    event = await edit_or_reply(event, "جاري فحص سرعة البوت...")

    animation_chars =[

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ ",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎📶‎‎📶📶‎📶‎📶‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶
        "⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ ",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎📶‎‎📶📶‎📶‎📶‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶‎⬛⬛‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛‎⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n‎⬛📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶⬛‎📶‎📶‎📶‎📶‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶⬛‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶⬛‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶‎⬛⬛‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛‎⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n‎⬛📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶⬛‎📶‎📶‎📶‎📶‎📶⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶⬛‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛",

        "⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛ \n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛ \n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛ \n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛ \n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛ \n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛ \n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛ \n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n⬛‎📶⬛‎📶‎📶‎📶‎📶‎📶⬛ \n⬛⬛⬛⬛⬛⬛⬛⬛⬛\n \n  ↫ البينغ بأفضل حالاته",

    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 26])

    end = datetime.now()

    ms = (end - start).microseconds / 1000

    await event.edit(
        f"‎‎‎‎‎‎‎‎‎⬛⬛⬛⬛⬛⬛⬛⬛⬛\n⬛‎📶‎📶‎📶‎📶‎📶‎📶‎📶⬛\n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛\n⬛⬛⬛⬛‎📶⬛⬛‎📶⬛\n⬛⬛⬛⬛⬛‎📶‎📶⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛⬛\n⬛📶‎‎📶📶‎📶‎📶‎📶‎📶⬛\n⬛‎⬛⬛📶‎📶‎⬛⬛📶⬛\n⬛‎⬛📶‎⬛📶⬛‎⬛📶⬛\n⬛📶‎⬛⬛⬛📶‎📶‎⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛⬛\n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛\n⬛📶‎⬛⬛⬛⬛⬛‎📶⬛\n⬛📶‎⬛⬛⬛‎⬛⬛📶‎⬛\n⬛📶‎⬛⬛‎⬛⬛⬛📶‎⬛\n⬛‎⬛📶‎📶‎📶‎📶‎📶‎⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛⬛\n⬛‎📶⬛‎📶‎📶‎📶‎📶‎📶⬛\n⬛⬛⬛⬛⬛⬛⬛⬛⬛ \n‎‎‎‎‎‎‎‎‎ \n \n My 🇵 🇮 🇳 🇬  Is : {ms} ms"
        )

