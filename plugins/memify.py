from command import mmf_cmd
from helpers import CMD

__MODULES__ = "Memify"
__HELP__ = """<blockquote>Command Help **Memifiy**</blockquote> 
<blockquote expandable>--**Basic Commands**--

    **Add text on top the sticker**
        `{0}mmf text` (reply sticker)
    **Add text on bottom the sticker**
        `{0}mmf ;text` (reply sticker)</blockquote>
<b>   {1}</b>
"""
__CATEGORY__ = "Media 🎨"


@CMD.UBOT("mmf|memify")
async def _(client, message):
    return await mmf_cmd(client, message)
