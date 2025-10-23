from command import (addbcdb_cmd, addbl_cmd, bc_cmd, bcerror_cmd, cancel_cmd,
                     delbcdb_cmd, delbl_cmd, gcast_cmd, listbcdb_cmd,
                     listbl_cmd, sendinline_cmd, ucast_cmd)
from helpers import CMD

__MODULES__ = "Broadcast"
__HELP__ = """<blockquote>Command Help **Broadcast**</blockquote>
<blockquote expandable>--**Basic Commands**--

    **Send broadcast message to chats db**
        `{0}bc db` (text/reply text)
    **Send broadcast message to chats group**
        `{0}bc group` (text/reply text)
    **Send broadcast message to chats group and private**
        `{0}bc all` (text/reply text)
    **Send broadcast message to private chat**
        `{0}bc private` (text/reply text)
    **Cancel broadcast message, give taskid**
        `{0}cancel` (taskid)</blockquote>

<blockquote expandable>--**Blacklist Commands**--

    **Add chat to blacklist broadcast**
        `{0}addbl` (chatid)
    **Delete chat from blacklist broadcast**
        `{0}delbl` (chatid)
    **View all chat from blacklist broadcast**
        `{0}listbl`</blockquote>

<blockquote expandable>--**Bcdb Commands**--

    **Add chat to broadcast db**
        `{0}add-bcdb` (chatid)
    **Delete chat to broadcast db**
        `{0}del-bcdb` (chatid)
    **View all chats on broadcast db**
        `{0}list-bcdb`</blockquote>
<b>   {1}</b>
"""
__CATEGORY__ = "Automation 📡"


@CMD.UBOT("bc", fakedevcmd=True)
async def _(client, message):
    return await bc_cmd(client, message)


@CMD.UBOT("gcast", fakedevcmd=True)
async def _(client, message):
    return await gcast_cmd(client, message)


@CMD.UBOT("ucast", fakedevcmd=True)
async def _(client, message):
    return await ucast_cmd(client, message)


@CMD.UBOT("bc-error", fakedevcmd=True)
async def _(client, message):
    return await bcerror_cmd(client, message)


@CMD.UBOT("cancel", fakedevcmd=True)
async def _(client, message):
    return await cancel_cmd(client, message)


@CMD.UBOT("addbl", multicmd=True)
async def _(client, message):
    return await addbl_cmd(client, message)


@CMD.UBOT("delbl", multicmd=True)
async def _(client, message):
    return await delbl_cmd(client, message)


@CMD.UBOT("listbl", multicmd=True)
async def _(client, message):
    return await listbl_cmd(client, message)


@CMD.UBOT("add-bcdb")
async def _(client, message):
    return await addbcdb_cmd(client, message)


@CMD.UBOT("del-bcdb")
async def _(client, message):
    return await delbcdb_cmd(client, message)


@CMD.UBOT("list-bcdb")
async def _(client, message):
    return await listbcdb_cmd(client, message)


@CMD.UBOT("send")
async def _(client, message):
    return await sendinline_cmd(client, message)
