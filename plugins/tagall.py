__MODULES__ = "Tagall"
__HELP__ = """<blockquote>Command Help **Tagall**</blockquote>
<blockquote expandable>--**Basic Commands**--

    **Tag member from chat**
        `{0}tagall` (text/reply text)
    **Tag only admins from chat**
        `@admins` (text/reply text)
    **Stop task tag**
        `{0}cancel` (taskid)</blockquote>
<b>   {1}</b>
"""
__CATEGORY__ = "Chat 💬"

from command import all_cmd, tagadmins_cmd
from helpers import CMD

IS_BASIC = True


@CMD.UBOT("all|tagall", group=True)
async def _(client, message):
    return await all_cmd(client, message)


@CMD.UBOT_REGEX(r"^(@admins)")
async def _(client, message):
    return await tagadmins_cmd(client, message)
