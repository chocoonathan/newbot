__MODULES__ = "Copy"
__HELP__ = """<blockquote>Command Help **Copy**</blockquote>
<blockquote expandable>--**Basic Commands**--

    **This command can steal or get message**
        `{0}copymsg`.</blockquote>
<b>   {1}</b>
"""


from command import copyall_cmd
from helpers import CMD

IS_BASIC = True
__CATEGORY__ = "Automation 📡"


@CMD.UBOT("copymsg")
async def _(client, message):
    return await copyall_cmd(client, message)
