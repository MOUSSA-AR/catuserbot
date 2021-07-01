import asyncio
import os
import sys
from asyncio.exceptions import CancelledError

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import HEROKU_APP, UPSTREAM_REPO_URL, catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import delgvar

plugin_category = "tools"
cmdhd = Config.COMMAND_HAND_LER

LOGS = logging.getLogger(__name__)
# -- Constants -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "لم يتم العثور على تطبيق هيروكو ، ولكن تم إعطاء مفتاح؟ 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "إعادة تشغيل تطبيق هيروكو."
IS_SELECTED_DIFFERENT_BRANCH = (
    "يبدو وكأنه فرع مخصص {branch_name} "
    "يتم استخدامه:\n"
    "غير قادر على تحديد الفرع المراد تحديثه."
    "يرجى مراجعة الفرع الرسمي وإعادة التحديث."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`سجل التغيير كبير جدًا ، اعرض الملف لرؤيته.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    sandy = await event.edit(
        "`تم تحديث البوت بنجاح!\n" "يتم إعادة تشغيل البوت.... الرجاء الإنتظار لحظة!`"
    )
    await event.client.reload(sandy)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit("`يرجى إعداد قيمة `  **HEROKU_API_KEY** ")
    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(
            "`يرجى إعداد قيمة` **HEROKU_APP_NAME** "
            " لتتمكن من نشر اليوزر بوت على حسابك...`"
        )
        repo.__del__()
        return
    for app in heroku_applications:
        if app.name == HEROKU_APP_NAME:
            heroku_app = app
            break
    if heroku_app is None:
        await event.edit(
            f"{txt}\n" "`البيانات التي ادخلتها في هيروكو غير صالحة للنشر.`"
        )
        return repo.__del__()
    sandy = await event.edit(
        "`قيد التقدم...يرجى الإنتظار لعدة دقائق`"
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("اعادة تحديث")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("اعادة تحديث", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace(
        "https://", "https://api:" + HEROKU_API_KEY + "@"
    )
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**Error log:**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edit_Delete(
            event, "`فشل الإنشاء!\n" "تم إلغائه أو أن هناك بعض الأخطاء...`"
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**هنا سجل خطأ:**\n`{error}`")
        return repo.__del__()
    await event.edit("`فشل النشر. قم بإعادة التشغيل للتحديث`")
    delgvar("ipaddress")
    try:
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()
    except CancelledError:
        pass


@catub.cat_cmd(
    pattern="تحديث(| الآن)?$",
    command=("تحديث", plugin_category),
    info={
        "header": "لتحديث يوزر بوت برو.",
        "description": "انصحك بإجراء تحديث نشر مرة واحدة على الأقل في الأسبوع.",
        "options": {
            "الآن": "سيتم تحديث البوت برو. لكن المطلبات لن يتم تحديثها.",
            "نشر": "سيتم تحديث البوت برو بالكامل. مع المطلبات أيضا.",
        },
        "usage": [
            "{tr}update",
            "{tr}update now",
            "{tr}update deploy",
        ],
    },
)
async def upstream(event):
    "للتحقق ما إذا كان البوت برو محدث"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "`يتم البحث عن تحديثات الرجاء الإنتظار....`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await edit_or_reply(
            event, "`قم بتعيين المتغيرات المطلوبة أولا لتحديث البوت!`"
        )
    try:
        txt = "`عفوا... لا يمكن للمحدث المتابعة لسبب ما!`"
        txt += "حدثت بعض المشاكل في تتبع السجل`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`لسوء الحظ, حدث خطأ {error} "
                "الدليل لا يبدو أنه مستودع.\n"
                "ولكن يمكننا إصلاح ذلك من خلال استخدام الأمر : "
                ".تحديث الآن`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`يبدو أنك تستخدم الفرع المخصص الخاص بك ({ac_br}). "
            "في هذه الحالة ، يتعذر على المحدث التعرف "
            "أي فرع سيتم دمجه. "
            "يرجى تسجيل الخروج في أي فرع رسمي`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if changelog == "" and not force_update:
        await event.edit(
            "\n`البوت برو`  **محدث بالفعل**  ``  "
            f"**{UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            f"do `{cmdhd}تحديث النشر` لتحديث النشر في يوزر بوت برو"
        )

    if force_update:
        await event.edit(
            "`فرض المزامنة مع أحدث كود مستخدم ثابت ، برجاء الانتظار ...`"
        )
    if conf == "now":
        await event.edit("`جاري تحديث البوت برو، الرجاء الإنتظار`")
        await update(event, repo, ups_rem, ac_br)
    return


@catub.cat_cmd(
    pattern="تحديث النشر$",
)
async def upstream(event):
    event = await edit_or_reply(event, "`جاري سحب الريبو انتظر ثانية...`")
    off_repo = "https://github.com/Mr-confused/nekopack"
    os.chdir("/app")
    try:
        txt = "`عفوًا .. لا يمكن للبوت متابعة التحديث لسبب ما..."
        txt += "حدثت بعض المشاكل...جاري تتبع السجل`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`الدليل {error} غير موجود`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`فشل مبكر! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("`جاري نشر يوزر بوت برو, الرجاء الإنتظار....`")
    await deploy(event, repo, ups_rem, ac_br, txt)


@catub.cat_cmd(
    pattern="قط سيئ$",
    command=("قط سيئ", plugin_category),
    info={
        "header": "للتحديث إلى بوت القط السيئ( للحصول على ميزات إضافية).",
        "usage": "{tr}badcat",
    },
)
async def variable(var):
    "للتحديث إلى القط السيئ( للحصول على ميزات إضافية)."
    if Config.HEROKU_API_KEY is None:
        return await edit_delete(
            var,
            "قم بتعيين هذه القيمة في هيروكو لتعمل بشكل جيد `HEROKU_API_KEY`.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit_delete(
            var,
            "قم بتعيين هذه القيمة في هيروكو لتعمل بشكل جيد `HEROKU_APP_NAME`.",
        )
    heroku_var = app.config()
    await edit_or_reply(var, f"`جاري التغيير من القط الجيد إلى القط السيئ... قد يستغرق بضعة دقائق`")
    heroku_var["UPSTREAM_REPO"] = "https://github.com/MOUSSA-AR/moussa-bot"
