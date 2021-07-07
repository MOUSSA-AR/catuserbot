# هاذه الوحدة مسؤولة عن الحذف في التلغرام.

import re

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from telethon.tl.types import (

    InputMessagesFilterDocument,

    InputMessagesFilterEmpty,

    InputMessagesFilterGeo,

    InputMessagesFilterGif,

    InputMessagesFilterMusic,

    InputMessagesFilterPhotos,

    InputMessagesFilterRoundVideo,

    InputMessagesFilterUrl,

    InputMessagesFilterVideo,

    InputMessagesFilterVoice,

)

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

from ..helpers.utils import reply_id

from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"

purgelist = {}

purgetype = {

    "a": InputMessagesFilterVoice,

    "f": InputMessagesFilterDocument,

    "g": InputMessagesFilterGif,

    "i": InputMessagesFilterPhotos,

    "l": InputMessagesFilterGeo,

    "m": InputMessagesFilterMusic,

    "r": InputMessagesFilterRoundVideo,

    "t": InputMessagesFilterEmpty,

    "u": InputMessagesFilterUrl,

    "v": InputMessagesFilterVideo,

    # "s": search

}

@catub.cat_cmd(

    pattern="احذف(\s*| \d+)$",

    command=("احذف", plugin_category),

    info={

        "header": "لحذف الرسالة التي يتم الرد عليها",

        "description": "تستخدم لحذف الرسالة التي يتم الرد عليها بعد الفترة الزمنية المحددة. وفي حال لم يتم وضع مهلة فسيقوم بحذفها على الفور",

        "usage": ["{tr}احذف <الوقت بالثواني>", "{tr}احذف"],

        "examples": "{tr}احذف 2",

    },

)

async def delete_it(event):

    "لحذف الرسالة التي يتم الرد عليها."

    input_str = event.pattern_match.group(1).strip()

    msg_src = await event.get_reply_message()

    if msg_src:

        if input_str and input_str.isnumeric():

            await event.delete()

            await sleep(int(input_str))

            try:

                await msg_src.delete()

                if BOTLOG:

                    await event.client.send_message(

                        BOTLOG_CHATID, "#حذف \n`تم حذف الرسالة بنجاح🧸🍁`"

                    )

            except rpcbaseerrors.BadRequestError:

                if BOTLOG:

                    await event.client.send_message(

                        BOTLOG_CHATID,

                        "`اعتدر لا يمكنني حذف هذه الرسالة. لأنني لست ادمن`",

                    )

        elif input_str:

            if not input_str.startswith("var"):

                await edit_or_reply(event, "`عذرا. الوقت الذي ذكرته غير صالح.`")

        else:

            try:

                await msg_src.delete()

                await event.delete()

                if BOTLOG:

                    await event.client.send_message(

                        BOTLOG_CHATID, "#حذف \n`تم حذف الرسالة بنجاح🧸🍁`"

                    )

            except rpcbaseerrors.BadRequestError:

                await edit_or_reply(event, "`عذرا، لا يمكنني حذف هذه الرسالة.`")

    elif not input_str:

        await event.delete()

@catub.cat_cmd(

    pattern="$حذف من",

    command=("حذف من", plugin_category),

    info={

        "header": "لوضع علامة على الرسالة التي تم الرد عليها كرسالة بداية لقائمة المسح.",

        "description": "بعد استخدام هذا الامر ، يجب استخدام الأمر (.حذف الى) أيضًا حتى يتم حذف الرسائل الموجودة بينهما.",

        "usage": "{tr}حذف من",

    },

)

async def purge_from(event):

    "لمسح الرسالة بالرد عليها"

    reply = await event.get_reply_message()

    if reply:

        reply_message = await reply_id(event)

        purgelist[event.chat_id] = reply_message

        await edit_delete(

            event,

            "`تم وضع علامة على هذه الرسالة للحذف. الآن قم بالرد على رسالة أخرى مع الرمز (.حذف الى) لحذف جميع الرسائل بينهما.`",

        )

    else:

        await edit_delete(event, "`يرجى الرد على الرسالة لمعرفة ماذا علي حذفه.`")

@catub.cat_cmd(

    pattern="حذف الى$",

    command=("حذف الى", plugin_category),

    info={

        "header": "لوضع علامة على الرسالة الثانية. كرسالة نهائية لقائمة الحذف.",

        "description": "تحتاج إلى استخدام الأمر (.حذف من) قبل أن تستخدف هذا الأمر. لحذف الرسائل بينهما.",

        "usage": "{tr}حذف الى",

    },

)

async def purge_to(event):

    "لمسح الرسالة بالرد عليها."

    chat = await event.get_input_chat()

    reply = await event.get_reply_message()

    try:

        from_message = purgelist[event.chat_id]

    except KeyError:

        return await edit_delete(

            event,

            "`قم بالرد على الرسالة الثانية بالأمر (.حذف الى) لكي تتمكن من حذف الرسائل بينهما.`",

        )

    if not reply or not from_message:

        return await edit_delete(

            event,

            "`اولاً. قم بالرد على الرسالة الأولى باستخدام الأمر (.حذف من) وبعدها قم بالرد على رسالة اخرى بالرمز (.حذف الى) لكي تتمكن من حذف الرسائل بينهما.`",

        )

    try:

        to_message = await reply_id(event)

        msgs = []

        count = 0

        async for msg in event.client.iter_messages(

            event.chat_id, min_id=(from_message - 1), max_id=(to_message + 1)

        ):

            msgs.append(msg)

            count += 1

            msgs.append(event.reply_to_msg_id)

            if len(msgs) == 100:

                await event.client.delete_messages(chat, msgs)

                msgs = []

        if msgs:

            await event.client.delete_messages(chat, msgs)

        await edit_delete(

            event,

            "`اكتمل الحذف!\nتم حذف " + str(count) + " من الرسائل",

        )

        if BOTLOG:

            await event.client.send_message(

                BOTLOG_CHATID,

                "#حذف\n`  تم حذف" + str(count) + "من الرسائل`",

            )

    except Exception as e:

        await edit_delete(event, f"**خطأ**\n`{str(e)}`")

@catub.cat_cmd(

    pattern="امسح",

    command=("امسح", plugin_category),

    info={

        "header": "حذف رسائلك الحديثة فقط.",

        "description": "عند استخدام الامر وبعده رقم فسيقوم بحذف العدد المطلوب من رسائلك الحديثة. اما في حال عدم وضع رقم فسيتم حذف جميع رسائلك الحديثة.",

        "usage": "{tr}امسح <العدد>",

        "examples": "{tr}امسح 2",

    },

)

async def purgeme(event):

    "لمسح رسائلك الحديثة فقط."

    message = event.text

    count = int(message[9:])

    i = 1

    async for message in event.client.iter_messages(event.chat_id, from_user="me"):

        if i > count + 1:

            break

        i += 1

        await message.delete()

    smsg = await event.client.send_message(

        event.chat_id,

        "**اكتمل المسح!**`تم مسح " + str(count) + " من الرسائل`",

    )

    if BOTLOG:

        await event.client.send_message(

            BOTLOG_CHATID,

            "#امسح \n`تم مسح " + str(count) + "من الرسائل بنجاح.`",

        )

    await sleep(5)

    await smsg.delete()

# TODO: only sticker messages.

@catub.cat_cmd(

    pattern="مسح(?:\s|$)([\s\S]*)",

    command=("مسح", plugin_category),

    info={

        "header": "باستخدام هذا الرمز يمكنك مسح جميع ما تحت الرسالة التي يتم الرد عليها.",

        "description": "•  باستخدام هذا الرمز مع عدد فإنه يقوم بمسح العدد المطلوب من الرسائل\

        \n•  اذا لم تستخدم رقم فإنه سيقوم بمسح جميع ما تحت الرسالة التي تم الرد عليها.\

        \n•  اذا لم تقم بالرد على اي رسالة فسيتم حذف الرسائل الاخيرة.\

        \n•  اذا لم تقم بالرد على اي رسالة او لم تستخدم اي ارقم او قيمة فلن يتم فعل شيئ.\

        \n•  اذا تم استخدام الكود ولم تحدد نوع الرسائل التي تريد حذفها فسيتم حذف جميع الرسائل\

        \n•  يمكنك استخدام اي قيمة مثل -gi 10 (سوف يقوم بحذف 10 صور فقط.)\

        ",

        "flags": {

            "a": "لمسح الرسائل الصوتية فقط.",

            "f": "لمسح الوثائق فقط.",

            "g": "لمسح الصور المتحركة فقط",

            "i": "لمسح الصور فقط.",

            "l": "لمسح المواقع فقط",

            "m": "لمسح مقاطع الصوت والملفات الموسيقية فقط.",

            "r": "لمسح مكالمات الفيديو فقط.",

            "t": "لمسح الستيكرز والنصوص فقط.",

            "u": "لمسح الروابط فقط.",

            "v": "لمسح الفيديوهات فقط.",

            "s": "",

        },

        "usage": [

            "{tr}مسح <القيمة(optional)> <رقم(x)> <رد على الرسالة> - لمسح عدد محدد من الرسائل المعينة",

            "{tr}مسح <القيمة> <رقم(x)> - لمسح عدد محدد من الرسائل المعينة",

        ],

        "examples": [

            "{tr}مسح 10",

            "{tr}مسح -f 10",

            "{tr}مسح -gi 10",

        ],

    },

)

async def fastpurger(event):  # sourcery no-metrics

    "مسح الرسائل بالرد عليها"

    chat = await event.get_input_chat()

    msgs = []

    count = 0

    input_str = event.pattern_match.group(1)

    ptype = re.findall(r"-\w+", input_str)

    try:

        p_type = ptype[0].replace("-", "")

        input_str = input_str.replace(ptype[0], "").strip()

    except IndexError:

        p_type = None

    error = ""

    result = ""

    await event.delete()

    reply = await event.get_reply_message()

    if reply:

        if input_str and input_str.isnumeric():

            if p_type is not None:

                for ty in p_type:

                    if ty in purgetype:

                        async for msg in event.client.iter_messages(

                            event.chat_id,

                            limit=int(input_str),

                            offset_id=reply.id - 1,

                            reverse=True,

                            filter=purgetype[ty],

                        ):

                            count += 1

                            msgs.append(msg)

                            if len(msgs) == 50:

                                await event.client.delete_messages(chat, msgs)

                                msgs = []

                        if msgs:

                            await event.client.delete_messages(chat, msgs)

                    elif ty == "s":

                        error += f"\n• __اذا لم تقم بالرد على اي رسالة ووضع عدد الرسائل. فسيتم مسح الرسائل الأخيرة.__"

                    else:

                        error += f"\n• `{ty}` __قيمة خاطئة.__"

            else:

                count += 1

                async for msg in event.client.iter_messages(

                    event.chat_id,

                    limit=(int(input_str) - 1),

                    offset_id=reply.id,

                    reverse=True,

                ):

                    msgs.append(msg)

                    count += 1

                    if len(msgs) == 50:

                        await event.client.delete_messages(chat, msgs)

                        msgs = []

                if msgs:

                    await event.client.delete_messages(chat, msgs)

        elif input_str and p_type is not None:

            if p_type == "s":

                try:

                    cont, inputstr = input_str.split(" ")

                except ValueError:

                    cont = "خطأ"

                    inputstr = input_str

                cont = cont.strip()

                inputstr = inputstr.strip()

                if cont.isnumeric():

                    async for msg in event.client.iter_messages(

                        event.chat_id,

                        limit=int(cont),

                        offset_id=reply.id - 1,

                        reverse=True,

                        search=inputstr,

                    ):

                        count += 1

                        msgs.append(msg)

                        if len(msgs) == 50:

                            await event.client.delete_messages(chat, msgs)

                            msgs = []

                else:

                    async for msg in event.client.iter_messages(

                        event.chat_id,

                        offset_id=reply.id - 1,

                        reverse=True,

                        search=input_str,

                    ):

                        count += 1

                        msgs.append(msg)

                        if len(msgs) == 50:

                            await event.client.delete_messages(chat, msgs)

                            msgs = []

                if msgs:

                    await event.client.delete_messages(chat, msgs)

            else:

                error += f"\n• `{ty}` __قيمة خاطئة.__"

        elif input_str:

            error += f"\n• `.مسح {input_str}` __فشل المسح. حاول مرة ثانية__ `.مساعدة مسح`"

        elif p_type is not None:

            for ty in p_type:

                if ty in purgetype:

                    async for msg in event.client.iter_messages(

                        event.chat_id,

                        min_id=event.reply_to_msg_id - 1,

                        filter=purgetype[ty],

                    ):

                        count += 1

                        msgs.append(msg)

                        if len(msgs) == 50:

                            await event.client.delete_messages(chat, msgs)

                            msgs = []

                    if msgs:

                        await event.client.delete_messages(chat, msgs)

                else:

                    error += f"\n• `{ty}` __قيمة خاطئة.__"

        else:

            async for msg in event.client.iter_messages(

                chat, min_id=event.reply_to_msg_id - 1

            ):

                count += 1

                msgs.append(msg)

                if len(msgs) == 50:

                    await event.client.delete_messages(chat, msgs)

                    msgs = []

            if msgs:

                await event.client.delete_messages(chat, msgs)

    elif p_type is not None and input_str:

        if p_type != "s" and input_str.isnumeric():

            for ty in p_type:

                if ty in purgetype:

                    async for msg in event.client.iter_messages(

                        event.chat_id, limit=int(input_str), filter=purgetype[ty]

                    ):

                        count += 1

                        msgs.append(msg)

                        if len(msgs) == 50:

                            await event.client.delete_messages(chat, msgs)

                            msgs = []

                    if msgs:

                        await event.client.delete_messages(chat, msgs)

                elif ty == "s":

                    error += f"\n• __.لا يمكنك استخدام s من الاوامر الأخدام__"

                else:

                    error += f"\n• `{ty}` __قيمة خاطئة.__"

        elif p_type == "s":

            try:

                cont, inputstr = input_str.split(" ")

            except ValueError:

                cont = "خطأ"

                inputstr = input_str

            cont = cont.strip()

            inputstr = inputstr.strip()

            if cont.isnumeric():

                async for msg in event.client.iter_messages(

                    event.chat_id, limit=int(cont), search=inputstr

                ):

                    count += 1

                    msgs.append(msg)

                    if len(msgs) == 50:

                        await event.client.delete_messages(chat, msgs)

                        msgs = []

            else:

                async for msg in event.client.iter_messages(

                    event.chat_id, search=input_str

                ):

                    count += 1

                    msgs.append(msg)

                    if len(msgs) == 50:

                        await event.client.delete_messages(chat, msgs)

                        msgs = []

            if msgs:

                await event.client.delete_messages(chat, msgs)

        else:

            error += f"\n• `{ty}` __قيمة خاطئة.__"

    elif p_type is not None:

        for ty in p_type:

            if ty in purgetype:

                async for msg in event.client.iter_messages(

                    event.chat_id, filter=purgetype[ty]

                ):

                    count += 1

                    msgs.append(msg)

                    if len(msgs) == 50:

                        await event.client.delete_messages(chat, msgs)

                        msgs = []

                if msgs:

                    await event.client.delete_messages(chat, msgs)

            elif ty == "s":

                error += f"\n• __لا يمكنك استخدام s من الاوامر الأخرى__"

            else:

                error += f"\n• `{ty}` __قيمة خاطئة.__"

    elif input_str.isnumeric():

        async for msg in event.client.iter_messages(chat, limit=int(input_str) + 1):

            count += 1

            msgs.append(msg)

            if len(msgs) == 50:

                await event.client.delete_messages(chat, msgs)

                msgs = []

        if msgs:

            await event.client.delete_messages(chat, msgs)

    else:

        error += "\n•  __لم يتم تحديد شيء إعادة فحص المساعدة__ (`.مساعدة مسح`)"

    if msgs:

        await event.client.delete_messages(chat, msgs)

    if count > 0:

        result += "__اكتمل المسح!\nتم مسح __`" + str(count) + "` __من الرسائل بنجاح.__"

    if error != "":

        result += f"\n\n**خطأ**{error}"

    if result == "":

        result += "__هذه الرسالة لا يمكن مسحها.__"

    hi = await event.client.send_message(event.chat_id, result)

    if BOTLOG:

        await event.client.send_message(

            BOTLOG_CHATID,

            f"#مسح \n{result}",

        )

    await sleep(5)

    await hi.delete()

@catub.cat_cmd(

    pattern="مسح2( -a)?(?:\s|$)([\s\S]*)",

    command=("مسح2", plugin_category),

    info={

        "header": "لتنقية الرسائل من الرسالة المدفوعة من المستخدم الأجبر..",

        "description": "• حذف مبلغ X (عدد) من الرسائل من رسالة المستخدم الرابحة\

        \n•  إذا كنت لا تستخدم العدد، فحذف جميع الرسائل من الرسائل المدفوعة من المستخدم الأجبر\

        \n•  استخدم -A Flag لحذف جميع رسائله أو ذكر X لحذف X رسائل حديثة له\

        \n•  استخدم علم -S لحذف جميع رسالته التي contatins التي تعطى كلمة.\

        \n•  لا يمكنك استخدام كلا العلامات في وقت واحد\

        ",

        "flags": {

            "a": "لحذف جميع رسائل المستخدم التي يرد عليها",

            "s": "لحذف جميع رسائل المستخدم.",

        },

        "usage": [

            "{tr}مسح2 <رقم> <رد علرسالة>",

            "{tr}مسح2 -a <رقم(optional)> <رد علرسالة>",

            "{tr}مسح2 -s <query> <رد علرسالة>",

        ],

        "examples": [

            "{tr}مسح2 10",

            "{tr}مسح2 -s fuck",

            "{tr}مسح2 -a",

        ],

    },

)

async def fast_purger(event):  # sourcery no-metrics

    "لتنقية الرسائل من الرسالة المدفوعة من المستخدم."

    chat = await event.get_input_chat()

    msgs = []

    count = 0

    flag = event.pattern_match.group(1)

    input_str = event.pattern_match.group(2)

    ptype = re.findall(r"-\w+", input_str)

    try:

        p_type = ptype[0].replace("-", "")

        input_str = input_str.replace(ptype[0], "").strip()

    except IndexError:

        p_type = None

    error = ""

    result = ""

    await event.delete()

    reply = await event.get_reply_message()

    if not reply or reply.sender_id is None:

        return await edit_delete(

            event, "**خطأ**\n__هذا الأمر يعمل فقط اذا قم بالرد على رسالة المستخدم.__"

        )

    if not flag:

        if input_str and p_type == "s":

            async for msg in event.client.iter_messages(

                event.chat_id,

                search=input_str,

                from_user=reply.sender_id,

            ):

                count += 1

                msgs.append(msg)

                if len(msgs) == 50:

                    await event.client.delete_messages(chat, msgs)

                    msgs = []

        elif input_str and input_str.isnumeric():

            async for msg in event.client.iter_messages(

                event.chat_id,

                limit=int(input_str),

                offset_id=reply.id - 1,

                reverse=True,

                from_user=reply.sender_id,

            ):

                msgs.append(msg)

                count += 1

                if len(msgs) == 50:

                    await event.client.delete_messages(chat, msgs)

                    msgs = []

        elif input_str:

            error += f"\n• `.مسح2 {input_str}` __فشل المسح حاول مرة ثانية__ `.مساعدة مسح`"

        else:

            async for msg in event.client.iter_messages(

                chat,

                min_id=event.reply_to_msg_id - 1,

                from_user=reply.sender_id,

            ):

                count += 1

                msgs.append(msg)

                if len(msgs) == 50:

                    await event.client.delete_messages(chat, msgs)

                    msgs = []

    elif input_str.isnumeric():

        async for msg in event.client.iter_messages(

            chat,

            limit=int(input_str),

            from_user=reply.sender_id,

        ):

            count += 1

            msgs.append(msg)

            if len(msgs) == 50:

                await event.client.delete_messages(chat, msgs)

                msgs = []

    else:

        async for msg in event.client.iter_messages(

            chat,

            from_user=reply.sender_id,

        ):

            count += 1

            msgs.append(msg)

            if len(msgs) == 50:

                await event.client.delete_messages(chat, msgs)

                msgs = []

    if msgs:

        await event.client.delete_messages(chat, msgs)

    if count > 0:

        result += "__اكتمل المسح!\nتم مسح __`" + str(count) + "` __من الرسائل بنجاح.__"

    if error != "":

        result += f"\n\n**خطأ:**{error}"

    if result == "":

        result += "__هذه الرسالة لا يمكن مسحها.__"

    hi = await event.client.send_message(event.chat_id, result)

    if BOTLOG:

        await event.client.send_message(

            BOTLOG_CHATID,

            f"#مسح2 \n{result}",

        )

    await sleep(5)

    await hi.delete()
