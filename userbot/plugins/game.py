import asyncio

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "fun"

game_code = ["ttt", "ttf", "cf", "rps", "rpsls", "rr", "c", "pc"]
button = ["0", "1", "2", "3", "4", "5", "6", "7"]
game_name = [
    "Tic-Tac-Toe",
    "Tic-Tac-Four",
    "Connect Four",
    "Rock-Paper-Scissors",
    "Rock-Paper-Scissors-Lizard-Spock",
    "Russian Roulette",
    "Checkers",
    "Pool Checkers",
]
game_list = "1.`ttt` :- Tic-Tac-Toe\n2.`ttf` :- Tic-Tac-Four\n3.`cf` :- Connect Four\n4.`rps` :- Rock-Paper-Scissors\n5.`rpsls` :- Rock-Paper-Scissors-Lizard-Spock\n6.`rr` :- Russian Roulette\n7.`c` :- Checkers\n8.`pc` :- Pool Checkers"


@catub.cat_cmd(
    pattern="لعبة(?:\s|$)([\s\S]*)",
    command=("لعبة", plugin_category),
    info={
        "header": "Play inline games",
        "description": "Start an inline game by inlinegamebot",
        "Game code & Name": {
            "ttt": "Tic-Tac-Toe",
            "ttf": "Tic-Tac-Four",
            "cf": "Connect Four",
            "rps": "Rock-Paper-Scissors",
            "rpsls": "Rock-Paper-Scissors-Lizard-Spock",
            "rr": "Russian Roulette",
            "c": "Checkers",
            "pc": "Pool Checkers",
        },
        "usage": "{tr}game <game code>",
        "examples": "{tr}game ttt ",
    },
)
async def igame(event):
    "Fun game by inline"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    data = dict(zip(game_code, button))
    name = dict(zip(game_code, game_name))
    if not input_str:
        await edit_delete(
            event, f"**رموز اللعبة المتاحة والأسماء :-**\n\n{game_list}", time=60
        )
        return
    if input_str not in game_code:
        catevent = await edit_or_reply(event, "`أعطني رمز اللعبة الصحيح...`")
        await asyncio.sleep(1)
        await edit_delete(
            catevent, f"**رموز اللعبة المتاحة والأسماء :-**\n\n{game_list}", time=60
        )
    else:
        game = data[input_str]
        gname = name[input_str]
        await edit_or_reply(
            event, f"**رمز اللعبة `{input_str}` تم اختياره للعبة:-** __{gname}__"
        )
        await asyncio.sleep(1)
        bot = "@inlinegamesbot"
        results = await event.client.inline_query(bot, gname)
        await results[int(game)].click(event.chat_id, reply_to=reply_to_id)
        await event.delete()
