__MODULES__ = "History"
__HELP__ = """<blockquote>Command Help **History** </blockquote>
<blockquote expandable>--**Basic Commands**--

    **Get history name from user you want**
        `{0}sg` (userid/username)</blockquote>
<b>   {1}</b>
"""
__CATEGORY__ = "User 👥"

from command import sangmata_cmd
from helpers import CMD


@CMD.UBOT("sg")
async def _(client, message):
    return await sangmata_cmd(client, message)
