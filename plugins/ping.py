from command import absen_cmd, mping_cmd, settext_cmd
from helpers import CMD


@CMD.UBOT("set_text")
async def _(client, message):
    return await settext_cmd(client, message)


@CMD.UBOT("ping", multicmd=True)
async def _(client, message):
    return await mping_cmd(client, message)


@CMD.UBOT("absen", fakedevcmd=True, devcmd=True)
async def _(client, message):
    return await absen_cmd(client, message)
