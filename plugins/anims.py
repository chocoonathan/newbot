from command import (adadino_cmd, ange_cmd, anjg_cmd, awk_cmd, babi_cmd,
                     bundir_cmd, hack_cmd, heli_cmd, hmmm_cmd, kntl_cmd,
                     kocokk_cmd, lipkoll_cmd, lopeyu_cmd, nahh_cmd, nakall_cmd,
                     peace_cmd, pns_cmd, rumah_cmd, sponge_cmd, syg_cmd,
                     tank_cmd, tembak_cmd, tq_cmd, ysaja_cmd)
from helpers import CMD

DEFAULTUSER = "Nay"


NOBLE = [
    "╲╲╲┏━━┓╭━━━╮╱╱╱\n╲╲╲┗┓┏┛┃╭━╮┃╱╱╱\n╲╲╲╲┃┃┏┫┃╭┻┻┓╱╱\n╱╱╱┏╯╰╯┃╰┫┏━╯╱╱\n╱╱┏┻━┳┳┻━┫┗┓╱╱╱\n╱╱╰━┓┃┃╲┏┫┏┛╲╲╲\n╱╱╱╱┃╰╯╲┃┃┗━╮╲╲\n╱╱╱╱╰━━━╯╰━━┛╲╲",
    "┏━╮\n┃▔┃▂▂┏━━┓┏━┳━━━┓\n┃▂┣━━┻━╮┃┃▂┃▂┏━╯\n┃▔┃▔╭╮▔┃┃┃▔┃▔┗━┓\n┃▂┃▂╰╯▂┃┗╯▂┃▂▂▂┃\n┃▔┗━━━╮┃▔▔▔┃▔┏━╯\n┃▂▂▂▂▂┣╯▂▂▂┃▂┗━╮\n┗━━━━━┻━━━━┻━━━┛",
    "┏┓┏━┳━┳━┳━┓\n┃┗┫╋┣┓┃┏┫┻┫\n┗━┻━┛┗━┛┗━┛\n────­­­­­­­­­YOU────",
    "╦──╔╗─╗╔─╔ ─\n║──║║─║║─╠ ─\n╚═─╚╝─╚╝─╚ ─\n╦─╦─╔╗─╦╦   \n╚╦╝─║║─║║ \n─╩──╚╝─╚╝",
    "╔══╗....<3 \n╚╗╔╝..('\\../') \n╔╝╚╗..( •.• ) \n╚══╝..(,,)(,,) \n╔╗╔═╦╦╦═╗ ╔╗╔╗ \n║╚╣║║║║╩╣ ║╚╝║ \n╚═╩═╩═╩═╝ ╚══╝",
    "░I░L░O░V░E░Y░O░U░",
    "┈┈╭━╱▔▔▔▔╲━╮┈┈┈\n┈┈╰╱╭▅╮╭▅╮╲╯┈┈┈\n╳┈┈▏╰┈▅▅┈╯▕┈┈┈┈\n┈┈┈╲┈╰━━╯┈╱┈┈╳┈\n┈┈┈╱╱▔╲╱▔╲╲┈┈┈┈\n┈╭━╮▔▏┊┊▕▔╭━╮┈╳\n┈┃┊┣▔╲┊┊╱▔┫┊┃┈┈\n┈╰━━━━╲╱━━━━╯┈╳",
    "╔ღ═╗╔╗\n╚╗╔╝║║ღ═╦╦╦═ღ\n╔╝╚╗ღ╚╣║║║║╠╣\n╚═ღ╝╚═╩═╩ღ╩═╝",
    "╔══╗ \n╚╗╔╝ \n╔╝(¯'v'¯) \n╚══'.¸./\n╔╗╔═╦╦╦═╗ ╔╗╔╗ \n║╚╣║║║║╩╣ ║╚╝║ \n╚═╩═╩═╩═╝ ╚══╝",
    "╔╗ \n║║╔═╦═╦═╦═╗ ╔╦╗ \n║╚╣╬╠╗║╔╣╩╣ ║║║ \n╚═╩═╝╚═╝╚═╝ ╚═╝ \n╔═╗ \n║═╬═╦╦╦═╦═╦═╦═╦═╗ \n║╔╣╬║╔╣╩╬╗║╔╣╩╣╔╝ \n╚╝╚═╩╝╚═╝╚═╝╚═╩╝",
    "╔══╗ \n╚╗╔╝ \n╔╝╚╗ \n╚══╝ \n╔╗ \n║║╔═╦╦╦═╗ \n║╚╣║║║║╚╣ \n╚═╩═╩═╩═╝ \n╔╗╔╗ ♥️ \n║╚╝╠═╦╦╗ \n╚╗╔╣║║║║ \n═╚╝╚═╩═╝",
    "╔══╗╔╗  ♡ \n╚╗╔╝║║╔═╦╦╦╔╗ \n╔╝╚╗║╚╣║║║║╔╣ \n╚══╝╚═╩═╩═╩═╝\n­­­─────­­­­­­­­­YOU─────",
    "╭╮╭╮╮╭╮╮╭╮╮╭╮╮ \n┃┃╰╮╯╰╮╯╰╮╯╰╮╯ \n┃┃╭┳━━┳━╮╭━┳━━╮ \n┃┃┃┃╭╮┣╮┃┃╭┫╭╮┃ \n┃╰╯┃╰╯┃┃╰╯┃┃╰┻┻╮ \n╰━━┻━━╯╰━━╯╰━━━╯",
    "┊┊╭━╮┊┊┊┊┊┊┊┊┊┊┊ \n━━╋━╯┊┊┊┊┊┊┊┊┊┊┊ \n┊┊┃┊╭━┳╮╭┓┊╭╮╭━╮ \n╭━╋━╋━╯┣╯┃┊┃╰╋━╯ \n╰━╯┊╰━━╯┊╰━┛┊╰━━",
]

__CATEGORY__ = "Fun 🎮"
__MODULES__ = "Animasi"
__HELP__ = """<blockquote>Command Help **Animasi**</blockquote>
<blockquote expandable>--**Basic Commands**--

    **You can use this command for anims**
        **`{0}dino` | `{0}nakal` | `{0}ange` 
        `{0}kocok` | `{0}hack` | `{0}syg`
        `{0}kntl` | `{0}ajg` | `{0}heli`
        `{0}nah` | `{0}piss` | `{0}hmm`
        `{0}tank` | `{0}awk` | `{0}loveyou`
        `{0}lipkol` | `{0}rumah` | `{0}tembak`
        `{0}bundir` | `{0}y` | `{0}tq`**</blockquote>
<b>   {1}</b>
"""

IS_BASIC = True


@CMD.UBOT("loveyou")
async def _(client, message):
    return await lopeyu_cmd(client, message)


@CMD.UBOT("hmm")
async def _(client, message):
    return await hmmm_cmd(client, message)


@CMD.UBOT("kntl")
async def _(client, message):
    return await kntl_cmd(client, message)


@CMD.UBOT("penis")
async def _(client, message):
    return await pns_cmd(client, message)


@CMD.UBOT("heli")
async def _(client, message):
    return await heli_cmd(client, message)


@CMD.UBOT("tembak")
async def _(client, message):
    return await tembak_cmd(client, message)


@CMD.UBOT("bundir")
async def _(client, message):
    return await bundir_cmd(client, message)


@CMD.UBOT("awk")
async def _(client, message):
    return await awk_cmd(client, message)


@CMD.UBOT("y")
async def _(client, message):
    return await ysaja_cmd(client, message)


@CMD.UBOT("tank")
async def _(client, message):
    return await tank_cmd(client, message)


@CMD.UBOT("babi")
async def _(client, message):
    return await babi_cmd(client, message)


@CMD.UBOT("ange")
async def _(client, message):
    return await ange_cmd(client, message)


@CMD.UBOT("lipkol")
async def _(client, message):
    return await lipkoll_cmd(client, message)


@CMD.UBOT("nakal")
async def _(client, message):
    return await nakall_cmd(client, message)


@CMD.UBOT("piss")
async def _(client, message):
    return await peace_cmd(client, message)


@CMD.UBOT("spongebob")
async def _(client, message):
    return await sponge_cmd(client, message)


@CMD.UBOT("kocok")
async def _(client, message):
    return await kocokk_cmd(client, message)


@CMD.UBOT("dino")
async def _(client, message):
    return await adadino_cmd(client, message)


@CMD.UBOT("ajg")
async def _(client, message):
    return await anjg_cmd(client, message)


@CMD.UBOT("nah")
async def _(client, message):
    return await nahh_cmd(client, message)


@CMD.UBOT("tq")
async def _(client, message):
    return await tq_cmd(client, message)


@CMD.UBOT("rumah")
async def _(client, message):
    return await rumah_cmd(client, message)


@CMD.UBOT("syg")
async def _(client, message):
    return await syg_cmd(client, message)


@CMD.UBOT("hack")
async def _(client, message):
    return await hack_cmd(client, message)
