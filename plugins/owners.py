from clients import navy
from command import (add_prem_user, add_seller, cb_gitpull2, cb_shell,
                     cmd_eval, dne_plugins, seller_cmd, set_plan, un_prem_user,
                     un_seller)
from helpers import CMD


@CMD.UBOT("pro|lite|basic|addprem", seller=True)
async def _(client, message):
    return await add_prem_user(client, message)


@CMD.UBOT("set_plan", seller=True)
async def _(client, message):
    return await set_plan(client, message)


@CMD.UBOT("unprem", seller=True)
async def _(client, message):
    return await un_prem_user(client, message)


@CMD.UBOT("addseller", fake_devs=True)
async def _(client, message):
    return await add_seller(client, message)


@CMD.UBOT("unseller", fake_devs=True)
async def _(client, message):
    return await un_seller(client, message)


@CMD.UBOT("shell|sh", devs=True)
async def _(client: navy, message):
    return await cb_shell(client, message)


@CMD.UBOT("eval|ev|e", devs=True, devcmd=True)
async def _(client: navy, message):
    return await cmd_eval(client, message)


@CMD.UBOT("reboot|update|reload", fake_devs=True)
async def _(client: navy, message):
    return await cb_gitpull2(client, message)


@CMD.UBOT("seller", fake_devs=True)
async def _(client, message):
    return await seller_cmd(client, message)


@CMD.UBOT("enable|disable|disabled", devs=True)
async def _(client, message):
    return await dne_plugins(client, message)
