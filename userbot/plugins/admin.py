from asyncio import sleep

from telethon import functions

from telethon.errors import (

    BadRequestError,

    ImageProcessFailedError,

    PhotoCropSizeSmallError,

)

from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError

from telethon.tl.functions.channels import (

    EditAdminRequest,

    EditBannedRequest,

    EditPhotoRequest,

)

from telethon.tl.functions.users import GetFullUserRequest

from telethon.tl.types import (

    ChatAdminRights,

    ChatBannedRights,

    InputChatPhotoEmpty,

    MessageMediaPhoto,

)

from userbot import catub

from ..core.logger import logging

from ..core.managers import edit_delete, edit_or_reply

from ..helpers import media_type

from ..helpers.utils import _format, get_user_from_event

from ..sql_helper.mute_sql import is_muted, mute, unmute

from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============

PP_TOO_SMOL = "`الصورة صغيرة جداً`"

PP_ERROR = "`الفشل أثناء معالجة الصورة`"

NO_ADMIN = "`أنا لست مشرف!`"

NO_PERM = "`للأسف. ليس لدي أذونات كافية!`"

CHAT_PP_CHANGED = "`تغيرت صورة المحادثة`"

INVALID_MEDIA = "`امتداد غير صالح`"

BANNED_RIGHTS = ChatBannedRights(

    until_date=None,

    view_messages=True,

    send_messages=True,

    send_media=True,

    send_stickers=True,

    send_gifs=True,

    send_games=True,

    send_inline=True,

    embed_links=True,

)

UNBAN_RIGHTS = ChatBannedRights(

    until_date=None,

    send_messages=None,

    send_media=None,

    send_stickers=None,

    send_gifs=None,

    send_games=None,

    send_inline=None,

    embed_links=None,

)

LOGS = logging.getLogger(__name__)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

plugin_category = "admin"

# ================================================

@catub.cat_cmd(

    pattern="الصورة(تعديل|حذف)$",

    command=("الصورة", plugin_category),

    info={

        "header": "يستخدم لتغيير صورة المجموعة أو حذفها",

        "description": "قم بالرد على صورة لتغيير صورة المجموعة",

        "flags": {

            "تعديل": "لتغيير صورة المجموعة",

            "حذف": "لحذف صورة المجموعة",

        },

        "usage": [

            "{tr}الصورة تعديل <رد على الصورة>",

            "{tr}الصورة حذف",

        ],

    },

    groups_only=True,

    require_admin=True,

)

async def set_group_photo(event):  # sourcery no-metrics

    "لتغيير صورة المجموعة"

    flag = (event.pattern_match.group(1)).strip()

    if flag == "تعديل":

        replymsg = await event.get_reply_message()

        photo = None

        if replymsg and replymsg.media:

            if isinstance(replymsg.media, MessageMediaPhoto):

                photo = await event.client.download_media(message=replymsg.photo)

            elif "صورة" in replymsg.media.document.mime_type.split("/"):

                photo = await event.client.download_file(replymsg.media.document)

            else:

                return await edit_delete(event, INVALID_MEDIA)

        if photo:

            try:

                await event.client(

                    EditPhotoRequest(

                        event.chat_id, await event.client.upload_file(photo)

                    )

                )

                await edit_delete(event, CHAT_PP_CHANGED)

            except PhotoCropSizeSmallError:

                return await edit_delete(event, PP_TOO_SMOL)

            except ImageProcessFailedError:

                return await edit_delete(event, PP_ERROR)

            except Exception as e:

                return await edit_delete(event, f"**Error : **`{str(e)}`")

            process = "تم التحديث"

    else:

        try:

            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))

        except Exception as e:

            return await edit_delete(event, f"**Error : **`{str(e)}`")

        process = "تم الحذف"

        await edit_delete(event, "```**تم ازالة صورة المجموعة🧸🖤**```")

    if BOTLOG:

        await event.client.send_message(

            BOTLOG_CHATID,

            "#الصورة\n"

            f"**تم تغيير صورة المجموعة بنجاح🧸🖤**"

            f"CHAT: {event.chat.title}(`{event.chat_id}`)",

        )

@catub.cat_cmd(

    pattern="رفع ادمن(?:\s|$)([\s\S]*)",

    command=("رفع ادمن", plugin_category),

    info={

        "header": "لرفع احد الأعضاء في المجموعة إلى ادمن",

        "description": "يتم اعطاء حقوق الأدمن للعضو الذي تقوم بالرد عليه\

            \nNote : تحتاج الصلاحيات المناسبة للقيام بهذا الأمر",

        "usage": [

            "{tr}promote <userid/username/reply>",

            "{tr}promote <userid/username/reply> <custom title>",

        ],

    },

    groups_only=True,

    require_admin=True,

)

async def promote(event):

    "لرفع مسؤول في المجموعة"

    new_rights = ChatAdminRights(

        add_admins=False,

        invite_users=True,

        change_info=False,

        ban_users=True,

        delete_messages=True,

        pin_messages=True,

    )

    user, rank = await get_user_from_event(event)

    if not rank:

        rank = "Admin"

    if not user:

        return

    catevent = await edit_or_reply(event, "`Promoting...`")

    try:

        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))

    except BadRequestError:

        return await catevent.edit(NO_PERM)

    await catevent.edit("`تم رفع العضو ادمن بنجاح.`")

    if BOTLOG:

        await event.client.send_message(

            BOTLOG_CHATID,

            f"#رفع_ادمن\

            \nUSER: [{user.first_name}](tg://user?id={user.id})\

            \nCHAT: {event.chat.title} (`{event.chat_id}`)",

        )

@catub.cat_cmd(

    pattern="تنزيل ادمن(?:\s|$)([\s\S]*)",

    command=("تنزيل ادمن", plugin_category),

    info={

        "header": "ازالة العضو من لائحة الأدمنية",

        "description": "يزيل جميع حقوق الأدمن للعضو في المجموعة\

            \nNote : تحتاج إلى الحقوق المناسبة لهذا وكذلك يجب أن تكون مالكا أو المسؤول لتتمكن من استخدام هذا الأمر",

        "usage": [

            "{tr}demote <userid/username/reply>",

            "{tr}demote <userid/username/reply> <custom title>",

        ],

    },

    groups_only=True,

    require_admin=True,

)

async def demote(event):

    "لإزالة العضو من لائحة الأدمنية"

    user, _ = await get_user_from_event(event)

    if not user:

        return

    catevent = await edit_or_reply(event, "`Demoting...`")

    newrights = ChatAdminRights(

        add_admins=None,

        invite_users=None,

        change_info=None,

        ban_users=None,

        delete_messages=None,

        pin_messages=None,

    )

    rank = "admin"

    try:

        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))

    except BadRequestError:

        return await catevent.edit(NO_PERM)

    await catevent.edit("`تم ازالة العضو من لائحة الأدمنية بنجاح! حظ اوفر في المرة القادمة.`")

    if BOTLOG:

        await event.client.send_message(

            BOTLOG_CHATID,

            f"#DEMOTE\

            \nUSER: [{user.first_name}](tg://user?id={user.id})\

            \nCHAT: {event.chat.title}(`{event.chat_id}`)",

        )

@catub.cat_cmd(

    pattern"حظر(?:\s|$)([\s\S]*)",

    command=("حظر", plugin_category),

    info={

        "header": "هذا الأمر سيحظر العضو في المجموعة.",

        "description": "هذا الأمر سيقوم بإزالة العضو من المجموعة ولن يستطيع العودة\

            \nNote : تحتاج إلى الأذونات الكافية لإستخدام هذا الأمر.",

        "usage": [

            "{tr}ban <userid/username/reply>",

            "{tr}ban <userid/username/reply> <reason>",

        ],

    },

    groups_only=True,

    require_admin=True,

)

async def _ban_person(event):

    "حظر العضو في المجموعة"

    user, reason = await get_user_from_event(event)

    if not user:

        return

    if user.id == event.client.uid:

        return await edit_delete(event, "__لا يمكنك حظر هذا العضو.__")

    catevent = await edit_or_reply(event, "`تم حظر العضو!`")

    try:

        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))

    except BadRequestError:

        return await catevent.edit(NO_PERM)

    try:

        reply = await event.get_reply_message()

        if reply:

            await reply.delete()

    except BadRequestError:

        return await catevent.edit(

﻿            "`ليس لدي الأذونات الكافية. ولك لا يزال العضو محظور!`"

        )

    if reason:

        await catevent.edit(

            f"{_format.mentionuser(user.first_name ,user.id)}` is banned !!`\n**Reason : **`{reason}`"

        )

    else:

        await catevent.edit(

            f"{_format.mentionuser(user.first_name ,user.id)} `is banned !!`"

        )

    if BOTLOG:

        if reason:

            await event.client.send_message(

                BOTLOG_CHATID,

                f"#حظر\

                \nUSER: [{user.first_name}](tg://user?id={user.id})\

                \nCHAT: {event.chat.title}(`{event.chat_id}`)\

                \nREASON : {reason}",

            )

        else:

            await event.client.send_message(

                BOTLOG_CHATID,

                f"#حظر\

                \nUSER: [{user.first_name}](tg://user?id={user.id})\

                \nCHAT: {event.chat.title}(`{event.chat_id}`)",

            )

@catub.cat_cmd(

    pattern="رفع الحظر(?:\s|$)([\s\S]*)",

    command=("رفح الحظر", plugin_category),

    info={

        "header": "يقوم هذا الأمر برفع الحظر عن العضو في المجموعة.",

        "description": "رفع الحظر عن العضو بالمجموعة من خلال وضع الأمر وبجانبه معرف العضو\

            \nNote : تحتاج إلى الأذونات الكافية لإستخدام هذا الأمر",

        "usage": [

            "{tr}unban <userid/username/reply>",

            "{tr}unban <userid/username/reply> <reason>",

        ],

    },

    groups_only=True,

    require_admin=True,

)

async def nothanos(event):

    "رفع الحظر عن العضو"

    user, _ = await get_user_from_event(event)

    if not user:

        return

    catevent = await edit_or_reply(event, "`Unbanning...`")

    try:

        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))

        await catevent.edit(

            f"{_format.mentionuser(user.first_name ,user.id)} `تم رفع الحظر عن العضو بنجاح ومنحه فرصة أخرى.`"

        )

        if BOTLOG:

            await event.client.send_message(

                BOTLOG_CHATID,

                "#رفع_الحظر\n"

                f"USER: [{user.first_name}](tg://user?id={user.id})\n"

                f"CHAT: {event.chat.title}(`{event.chat_id}`)",

            )

    except UserIdInvalidError:

        await catevent.edit("`حظر العضو!`")

    except Exception as e:

        await catevent.edit(f"**Error :**\n`{e}`")

@catub.cat_cmd(incoming=True)

async def watcher(event):

    if is_muted(event.sender_id, event.chat_id):

        try:

            await event.delete()

        except Exception as e:

            LOGS.info(str(e))

@catub.cat_cmd(

    pattern="كتم(?:\s|$)([\s\S]*)",

    command=("كتم", plugin_category),

    info={

        "header": "ايقاف العضو عن ارسال الرسائل",

        "description": "اذا لم يكن مشرف في المجموعة بعد هذا يمكنه تغيير اذنه فيها,\

            إذا كان المسؤول أو إذا حاولت في الدردشة الشخصية، فسيتم حذف رسائلك\

            \nNote : تحتاج إلى الأذونات المطلوبة للقيام بهذا الأمر.",

        "usage": [

            "{tr}mute <userid/username/reply>",

            "{tr}mute <userid/username/reply> <reason>",

        ],

    },  # sourcery no-metrics

)

async def startmute(event):

    "لكتم العضو في المجموعة "

    if event.is_private:

        await event.edit("`قد تحدث مشكلات غير متوقعة أو أخطاء سيئة!`")

        await sleep(2)

        await event.get_reply_message()

        replied_user = await event.client(GetFullUserRequest(event.chat_id))

        if is_muted(event.chat_id, event.chat_id):

            return await event.edit(

                "`تم كتم هذا المستخدم بالفعل في هذه الدردشة~~lmfao sed rip~~`"

            )

        if event.chat_id == catub.uid:

            return await edit_delete(event, "`لا يمكنك كتم هذا العضو!`")

        try:

            mute(event.chat_id, event.chat_id)

        except Exception as e:

            await event.edit(f"**Error **\n`{str(e)}`")

        else:

            await event.edit("`تم كتم العضو بنجاح!.\n**ï½-Â´)âââï¾.*ï½¥ï½¡ï¾ **`")

        if BOTLOG:

            await event.client.send_message(

                BOTLOG_CHATID,

                "#PM_MUTE\n"

                f"**User :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",

            )

    else:

        chat = await event.get_chat()

        admin = chat.admin_rights

        creator = chat.creator

        if not admin and not creator:

            return await edit_or_reply(

                event, "`لا يمكنك كتم الأعضاء دون حقوق المسؤول!` à²¥ï¹à²¥  "

            )

        user, reason = await get_user_from_event(event)

        if not user:

            return

        if user.id == catub.uid:

            return await edit_or_reply(event, "`اعتذر, لا يمكنني حظر هذا العضو`")

        if is_muted(user.id, event.chat_id):

            return await edit_or_reply(

                event, "`تم كتم هذا المستخدم بالفعل في هذه الدردشة ~~lmfao sed rip~~`"

            )

        result = await event.client(

            functions.channels.GetParticipantRequest(event.chat_id, user.id)

        )

        try:

            if result.participant.banned_rights.send_messages:

                return await edit_or_reply(

                    event,

                    "`تم كتم هذا المستخدم بالفعل في هذه الدردشة ~~lmfao sed rip~~`",

                )

        except AttributeError:

            pass

        except Exception as e:

            return await edit_or_reply(event, f"**Error : **`{str(e)}`", 10)

        try:

            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))

        except UserAdminInvalidError:

            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:

                if chat.admin_rights.delete_messages is not True:

                    return await edit_or_reply(

                        event,

                        "`لا يمكنك كتم العضو إذا لم يكن لديك صلاحية حذف الرسائل. à²¥ï¹à²¥`",

                    )

            elif "creator" not in vars(chat):

                return await edit_or_reply(

                    event, "`لا يمكنك كتم الأعضاء اذا لم تكن ادمن!` à²¥ï¹à²¥  "

                )

            mute(user.id, event.chat_id)

        except Exception as e:

            return await edit_or_reply(event, f"**Error : **`{str(e)}`", 10)

        if reason:

            await edit_or_reply(

                event,

                f"{_format.mentionuser(user.first_name ,user.id)} `is muted in {event.chat.title}`\n"

                f"`Reason:`{reason}",

            )

        else:

            await edit_or_reply(

                event,

                f"{_format.mentionuser(user.first_name ,user.id)} `is muted in {event.chat.title}`\n",

            )

        if BOTLOG:

            await event.client.send_message(

                BOTLOG_CHATID,

                "#MUTE\n"

                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"

                f"**Chat :** {event.chat.title}(`{event.chat_id}`)",

            )

@catub.cat_cmd(

    pattern="رفع الكتم(?:\s|$)([\s\S]*)",

    command=("رفع الكتم", plugin_category),

    info={

        "header": "لرفع الكتم عن العضو والسماح له بإرسال الرسائل",

        "description": "سيتم السماح للعضو بإرسال الرسائل مرة اخرى\

        \nNote : تحتاج إلى الأذونات الكافية للقيام بهذا الأمر.",

        "usage": [

            "{tr}unmute <userid/username/reply>",

            "{tr}unmute <userid/username/reply> <reason>",

        ],

    },

)

async def endmute(event):

    "لرفع الكتم عن العضو في المجموعة."

    if event.is_private:

        await event.edit("`قد تحدث مشكلات غير متوقعة أو أخطاء سيئة!`")

        await sleep(1)

        replied_user = await event.client(GetFullUserRequest(event.chat_id))

        if not is_muted(event.chat_id, event.chat_id):

            return await event.edit(

                "`__هذا العضو ليس مكتوماً في المحادثة__\nï¼ ^_^ï¼oèªèªoï¼^_^ ï¼`"

            )

        try:

            unmute(event.chat_id, event.chat_id)

        except Exception as e:

            await event.edit(f"**Error **\n`{str(e)}`")

        else:

            await event.edit(

                "`تم رفع الكتم عن العضو بنجاح!\nä¹( â à±ªâ)ã    â(ï¿£Ð ï¿£)â`"

            )

        if BOTLOG:

            await event.client.send_message(

    ﻿            BOTLOG_CHATID,

                "#PM_UNMUTE\n"

                f"**User :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",

            )

    else:

        user, _ = await get_user_from_event(event)

        if not user:

            return

        try:

            if is_muted(user.id, event.chat_id):

                unmute(user.id, event.chat_id)

            else:

                result = await event.client(

                    functions.channels.GetParticipantRequest(event.chat_id, user.id)

                )

                if result.participant.banned_rights.send_messages:

                    await event.client(

                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)

                    )

        except AttributeError:

            return await edit_or_reply(

                event,

                "`هذا العضو اصبح بإمكانه إرسال الرسائل في المجوعة! ~~lmfao sed rip~~`",

            )

        except Exception as e:

            return await edit_or_reply(event, f"**Error : **`{str(e)}`")

        await edit_or_reply(

            event,

            f"{_format.mentionuser(user.first_name ,user.id)} `غير مكتوم في {event.chat.title}\nä¹( â à±ªâ)ã    â(ï¿£Ð ï¿£)â`",

        )

        if BOTLOG:

            await event.client.send_message(

                BOTLOG_CHATID,

                "#UNMUTE\n"

                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"

                f"**Chat :** {event.chat.title}(`{event.chat_id}`)",

            )

@catub.cat_cmd(

    pattern="طرد(?:\s|$)([\s\S]*)",

    command=("طرد", plugin_category),

    info={

        "header": "لطرد شخص من المجموعة",

        "description": "لطرد شخص من المجموعة ويكون بإمكانه العودة مرة أخرى.\

        \nNote : تحتاج إلى الأذونات الكافية للقيام بهذا الأمر.",

        "usage": [

            "{tr}kick <userid/username/reply>",

            "{tr}kick <userid/username/reply> <reason>",

        ],

    },

    groups_only=True,

    require_admin=True,

)

async def endmute(event):

    "يستخدم هذا الأمر لطرد العضو من المجموعة"

    user, reason = await get_user_from_event(event)

    if not user:

        return

    catevent = await edit_or_reply(event, "`Kicking...`")

    try:

        await event.client.kick_participant(event.chat_id, user.id)

    except Exception as e:

        return await catevent.edit(NO_PERM + f"\n{str(e)}")

    if reason:

        await catevent.edit(

            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"

        )

    else:

        await catevent.edit(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:

        await event.client.send_message(

            BOTLOG_CHATID,

            "#KICK\n"

            f"USER: [{user.first_name}](tg://user?id={user.id})\n"

            f"CHAT: {event.chat.title}(`{event.chat_id}`)\n",

        )

@catub.cat_cmd(

    pattern="تثبيت( مكتوم|$)",

    command=("تثبيت", plugin_category),

    info={

        "header": "لتثبيت رسالة في المحادثة",

        "description": "يستخدم هذا الأمر بالرد على الرسالة المراد تثبيتها ليتم تثبيتها في المحادثة\

        \nNote : تحتاج الا صلاحية تثبيت الرسائل في حال اردت استخدامها في المجموعات",

        "options": {"مكتوم": "لتثبيت الرسالة بصمت. دون ان يظهر اشعار لأحد."},

        "usage": [

            "{tr}تثبيت <reply>",

            "{tr}تثبيت مكتوم <reply>",

        ],

    },

)

async def pin(event):

    "لتثبيت الرسالة في المحادثة"

    to_pin = event.reply_to_msg_id

    if not to_pin:

        return await edit_delete(event, "`يجب الرد على الرسالة بالرمز تثبيتها`", 5)

    options = event.pattern_match.group(1)

    is_silent = bool(options)

    try:

        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)

    except BadRequestError:

        return await edit_delete(event, NO_PERM, 5)

    except Exception as e:

        return await edit_delete(event, f"`{str(e)}`", 5)

    await edit_delete(event, "`**تم التثبيت بنجاح!**`", 3)

    if BOTLOG and not event.is_private:

        await event.client.send_message(

            BOTLOG_CHATID,

            f"#PIN\

                \n__تم تثبيت الرسالة بنجاح__\

                \nCHAT: {event.chat.title}(`{event.chat_id}`)\

                \nLOUD: {is_silent}",

        )

@catub.cat_cmd(

    pattern="الغاء تثبيت( الكل|$)",

    command=("الغاء تثبيت", plugin_category),

    info={

        "header": "الغاء تثبيت الرسالة في المحادثة",

        "description": "يجب الرد على الرسالة بالأمر لتتمكن من الغاء تثبيتها!\

        \nNote : يجب ان يكون لديك صلاحية تثبيت الرسائل لتتمكن من استخدام الأمر في المجموعات.",

        "options": {"الكل": "لإلغاء تثبيت جميع الرسائل دفعة واحدة"},

        "usage": [

            "{tr}unpin <reply>",

            "{tr}unpin all",

        ],

    },

)

async def pin(event):

    "لإلغاء تثبيت الرسالة في المجموعة"

    to_unpin = event.reply_to_msg_id

    options = (event.pattern_match.group(1)).strip()

    if not to_unpin and options != "all":

        return await edit_delete(

            event,

            "__استخدم الرمز بالرد على الرسالة التي تريد الغاء تثبيتها __`.الغاء تثبيت الكل`__ لإلغاء تثبيت الرسائل__",

            5,

        )

    try:

        if to_unpin and not options:

            await event.client.unpin_message(event.chat_id, to_unpin)

        elif options == "الكل":

            await event.client.unpin_message(event.chat_id)

        else:

            return await edit_delete(

                event, "`استخدم الأمر (.الغاء تثبيت الكل) لتتمكن من الغاء تثبيت جميع الرسائل.`", 5

            )

    except BadRequestError:

        return await edit_delete(event, NO_PERM, 5)

    except Exception as e:

        return await edit_delete(event, f"`{str(e)}`", 5)

    await edit_delete(event, "`**تم الغاء تثبيت الرسالة بنجاح!**`", 3)

    if BOTLOG and not event.is_private:

        await event.client.send_message(

            BOTLOG_CHATID,

            f"#UNPIN\

                \n__**تم الغاء تثبيت جميع الرسائل بنجاح!**__\

                \nCHAT: {event.chat.title}(`{event.chat_id}`)",

        )

@catub.cat_cmd(

    pattern="المحذوفات( وسائط)?(?: |$)(\d*)?",

    command=("المحذوفات", plugin_category),

    info={

        "header": "للحصول على الرسائل المحذوفة الأخيرة في المجموعة",

        "description": "للتحقق من الرسائل المحذوفة الأخيرة في المجموعة، سيعرض بشكل افتراضي 5. يمكنك الحصول على 1 إلى 15 رسالة.",

        "flags": {

            "وسائط": "استخدم هذا الأمر لتحميل الوسائط لدردشة أخرى سوف تظهر فقط كوسيلة."

        },

        "usage": [

            "{tr}undlt <count>",

            "{tr}undlt -u <count>",

        ],

        "examples": [

            "{tr}undlt 7",

            "{tr}undlt -u 7 (هذا سوف يرد جميع الرسائل 7 لهذه الرسالة",

        ],

    },

    groups_only=True,

    require_admin=True,

)

async def _iundlt(event):  # sourcery no-metrics

    "لتفقد الرسائل المحذوفة في المجموعة"

    catevent = await edit_or_reply(event, "`Searching recent actions .....`")

    flag = event.pattern_match.group(1)

    if event.pattern_match.group(2) != "":

        lim = int(event.pattern_match.group(2))

        if lim > 15:

            lim = int(15)

        if lim <= 0:

            lim = int(1)

    else:

        lim = int(5)

    adminlog = await event.client.get_admin_log(

        event.chat_id, limit=lim, edit=False, delete=True

    )

    deleted_msg = f"**أحدث {lim} الرسائل المحذوفة في هذه المجموعة:**"

    if not flag:

        for msg in adminlog:

            ruser = (

                await event.client(GetFullUserRequest(msg.old.from_id.user_id))

            ).user

            _media_type = media_type(msg.old)

            if _media_type is None:

                deleted_msg += f"\nâ __{msg.old.message}__ **Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"

            else:

                deleted_msg += f"\nâ __{_media_type}__ **Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"

        await edit_or_reply(catevent, deleted_msg)

    else:

        main_msg = await edit_or_reply(catevent, deleted_msg)

        for msg in adminlog:

            ruser = (

                await event.client(GetFullUserRequest(msg.old.from_id.user_id))

            ).user

            _media_type = media_type(msg.old)

      ﻿      if _media_type is None:

                await main_msg.reply(

                    f"{msg.old.message}\n**Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"

                )

            else:

                await main_msg.reply(

                    f"{msg.old.message}\n**Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}",

                    file=msg.old.media,

                )
