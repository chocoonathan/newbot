import asyncio
import contextlib
import html
import io
import os
import subprocess
import sys
import traceback
import zipfile
from datetime import datetime
from inspect import getfullargspec, getmembers
from time import perf_counter
from typing import Any, List, Optional, Tuple

import pyrogram
import pyrogram.enums
import pyrogram.errors
import pyrogram.helpers
import pyrogram.raw
import pyrogram.types
import pyrogram.utils
from meval import meval
from pytz import timezone

import clients as clientsdb
import config
import database as databasedb
import helpers as helpersdb
from logs import logger


async def edit_or_reply(msg, **kwargs):
    client = msg._client
    func = msg.edit if not client.me.is_bot else msg.reply
    if hasattr(func, "__wrapped__"):
        spec = getfullargspec(func.__wrapped__).args
    else:
        spec = getfullargspec(func).args

    await func(**{k: v for k, v in kwargs.items() if k in spec})


helpers_vars = {
    name: obj for name, obj in getmembers(helpersdb) if not name.startswith("__")
}
clients_vars = {
    name: obj for name, obj in getmembers(clientsdb) if not name.startswith("__")
}
database_vars = {
    name: obj for name, obj in getmembers(databasedb) if not name.startswith("__")
}


def format_exception(
    exp: BaseException, tb: Optional[List[traceback.FrameSummary]] = None
) -> str:
    """Formats an exception traceback as a string, similar to the Python interpreter."""

    if tb is None:
        tb = traceback.extract_tb(exp.__traceback__)

    # Replace absolute paths with relative paths
    cwd = os.getcwd()
    for frame in tb:
        if cwd in frame.filename:
            frame.filename = os.path.relpath(frame.filename)

    stack = "".join(traceback.format_list(tb))
    msg = str(exp)
    if msg:
        msg = f": {msg}"

    return f"Traceback (most recent call last):\n{stack}{type(exp).__name__}{msg}"


async def send_ubot_1(client, message):
    user = message.from_user if message.from_user else message.sender_chat
    if user.id not in config.KYNAN:
        return
    return await client.send_message(
        message.from_user.id,
        await helpersdb.Message.userbot_list(0),
        reply_markup=helpersdb.ButtonUtils.account_list(0),
    )


async def send_ubot_2(client, message):
    user = message.from_user if message.from_user else message.sender_chat
    if user.id not in config.SUDO_OWNERS:
        return
    return await client.send_message(
        message.from_user.id,
        await helpersdb.Message.userbot_list(0),
        reply_markup=helpersdb.ButtonUtils.account_list(0),
    )


async def restore(client, message):
    user = message.from_user if message.from_user else message.sender_chat
    if user.id not in config.KYNAN:
        return
    reply = message.reply_to_message
    if not reply:
        return await message.reply("**Please reply to a .db or .zip file**")

    document = reply.document
    file_path = await client.download_media(document, "./")

    if file_path.endswith(".zip"):
        extract_path = "./extracted_db"
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        db_files = [f for f in os.listdir(extract_path) if f.endswith(".db")]
        if not db_files:
            return await message.reply("**No .db file found in the ZIP archive**")

        extracted_db = os.path.join(extract_path, db_files[0])
        if os.path.exists(databasedb.DB_PATH):
            os.remove(databasedb.DB_PATH)
        os.rename(extracted_db, databasedb.DB_PATH)

        os.remove(file_path)
    else:
        if os.path.exists(databasedb.DB_PATH):
            os.remove(databasedb.DB_PATH)
        document = reply.document
        file_path = await client.download_media(document, "./")
    await message.reply(
        f"<blockquote><b>Sukses melakukan restore database, tunggu sebentar bot akan me-restart.</blockquote></b>"
    )
    os.execl(sys.executable, sys.executable, *sys.argv)


async def backup(client, message):
    user = message.from_user if message.from_user else message.sender_chat
    if user.id not in config.KYNAN:
        return
    now = datetime.now(timezone("Asia/Jakarta"))
    timestamp = now.strftime("%Y-%m-%d_%H:%M")
    zip_filename = f"{config.BOT_NAME}_{timestamp}.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        if os.path.exists(".env"):
            env_path = os.path.abspath(".env")
            zipf.write(env_path, os.path.basename(env_path))
            zipf.write(databasedb.DB_PATH, os.path.basename(databasedb.DB_PATH))
        else:
            zipf.write(databasedb.DB_PATH, os.path.basename(databasedb.DB_PATH))
    caption = now.strftime("%d %B %Y %H:%M")
    return await message.reply_document(zip_filename, caption=caption)


async def cb_shell(client, message):
    user = message.from_user if message.from_user else message.sender_chat
    if user.id not in config.KYNAN:
        return
    if len(message.command) < 2:
        return await message.reply("Noob!!")
    cmd_text = message.text.split(maxsplit=1)[1]
    proses = await message.reply(f"__Executing shell {cmd_text}...__")
    text = f"<code>{cmd_text}</code>\n\n"
    start_time = perf_counter()

    try:
        stdout, stderr = await helpersdb.Tools.bash(cmd_text)
    except TimeoutError:
        text += "<b>Timeout expired!!</b>"
        await proses.delete()
        return await message.reply(text)
    finally:
        duration = perf_counter() - start_time
    if cmd_text.startswith("cat "):
        filepath = cmd_text.split("cat ", 1)[1].strip()
        output_filename = os.path.basename(filepath)
    else:
        output_filename = f"{cmd_text}.txt"
    if len(stdout) > 4096:
        await proses.edit("<b>Oversize, sending file...</b>")
        with open(output_filename, "w") as file:
            file.write(stdout)

        await message.reply_document(
            output_filename,
            caption=f"<b>Command completed in `{duration:.2f}` seconds.</b>",
        )
        os.remove(output_filename)
        return await proses.delete()
    else:
        text += f"<blockquote expandable><code>{stdout}</code></blockquote>"

        if stderr:
            text += f"<blockquote expandable>{stderr}</blockquote>"
        text += f"\n<b>Completed in `{duration:.2f}` seconds.</b>"
        await proses.delete()
        return await message.reply(text, parse_mode=pyrogram.enums.ParseMode.HTML)


async def cmd_eval(client, message):
    if not message.from_user:
        return
    if message.from_user.id not in config.KYNAN:
        return
    if (
        message.command and len(message.command) == 1
    ) or message.text == "client.run()":
        return await edit_or_reply(message, text="No Code!!")
    status_message = (
        await message.edit("<i>Processing eval pyrogram..</i>")
        if not client.me.is_bot
        else await message.reply("<i>Processing eval pyrogram..</i>", quote=True)
    )
    code = (
        message.text.split(maxsplit=1)[1]
        if message.command
        else message.text.split("\nclient.run()")[0]
    )
    out_buf = io.StringIO()
    out = ""

    async def _eval() -> Tuple[str, Optional[str]]:
        # helpersdb.Message sending helper for convenience
        async def send(*args: Any, **kwargs: Any):
            return await message.reply_msg(*args, **kwargs)

        # Print wrapper to capture output
        # We don't override sys.stdout to avoid interfering with other output
        def _print(*args: Any, **kwargs: Any):
            if "file" not in kwargs:
                kwargs["file"] = out_buf
            return print(*args, **kwargs)

        def _help(*args: Any, **kwargs: Any):
            with contextlib.redirect_stdout(out_buf):
                help(*args, **kwargs)

        eval_vars = {
            # PARAMETERS
            "c": client,
            "m": message,
            "u": (message.reply_to_message or message).from_user,
            "r": message.reply_to_message,
            "chat": message.chat,
            "p": _print,
            "h": _help,
            # PYROGRAM
            "asyncio": asyncio,
            "pyrogram": pyrogram,
            "raw": pyrogram.raw,
            "enums": pyrogram.enums,
            "types": pyrogram.types,
            "errors": pyrogram.errors,
            "utils": pyrogram.utils,
            "ph": pyrogram.helpers,
        }
        eval_vars.update(helpers_vars)
        eval_vars.update(clients_vars)
        eval_vars.update(database_vars)
        try:
            return "", await meval(code, globals(), **eval_vars)
        except Exception as e:  # skipcq: PYL-W0703
            # Find first traceback frame involving the snippet
            first_snip_idx = -1
            tb = traceback.extract_tb(e.__traceback__)
            for i, frame in enumerate(tb):
                if frame.filename == "<string>" or frame.filename.endswith("ast.py"):
                    first_snip_idx = i
                    break
            # Re-raise exception if it wasn't caused by the snippet
            # Return formatted stripped traceback
            stripped_tb = tb[first_snip_idx:]
            formatted_tb = format_exception(e, tb=stripped_tb)
            return "⚠️ Error while executing snippet\n\n", formatted_tb

    before = perf_counter()
    prefix, result = await _eval()
    after = perf_counter() - before
    # Always write result if no output has been collected thus far
    if not out_buf.getvalue() or result is not None:
        print(result, file=out_buf)

    out = out_buf.getvalue()
    if out.endswith("\n"):
        out = out[:-1]
    final_output = f"{prefix}<b>INPUT:</b>\n<pre language='python'>{html.escape(code)}</pre>\n<b>OUTPUT:</b>\n<pre language='python'>{html.escape(out)}</pre>\nExecuted Time: {after:.2f}s"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(out)) as out_file:
            out_file.name = f"{config.BOT_NAME}.txt"
            await message.reply_document(
                document=out_file,
                caption=f"<code>{code[: 4096 // 4 - 1]}</code>",
                disable_notification=True,
                reply_markup=pyrogram.helpers.ikb([[("Close", "close")]]),
                quote=True,
            )
            await status_message.delete()
    else:
        await edit_or_reply(
            message,
            text=final_output,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            reply_markup=pyrogram.helpers.ikb([[("Close", "close")]]),
            quote=True,
        )
        if client.me.is_bot:
            await status_message.delete()


async def send_large_output(message, output):
    with io.BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "update.txt"
        await message.reply_document(document=out_file)


async def update_kode_all(client, message):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await message.reply(f"<blockquote expandable>{out}</blockquote>")
    elif int(len(str(out))) > 4096:
        await send_large_output(message, out)
    else:
        await message.reply(f"<blockquote expandable>{out}</blockquote>")
    await message.reply("♻️ <i>Restarting untuk memuat perubahan...</i>")
    asyncio.create_task(helpersdb.restart_process())


async def cb_gitpull2(client, message):
    user = message.from_user if message.from_user else message.sender_chat
    if user.id not in config.SUDO_OWNERS:
        return
    if message.command[0] == "update":
        return await update_kode_all(client, message)
    elif message.command[0] == "reboot":
        await message.reply(
            "<b>✅ Bot stopped successfully. Trying to restart Userbot!!</b>"
        )
        asyncio.create_task(helpersdb.restart_process())


async def copymsg_bot(client, message):
    proses = await message.reply("<b>Please wait a minute...</b>")
    try:
        link = message.text.split()[1]
        if len(message.command) < 2:
            return await message.reply(
                f"<b><code>{message.text.split()[0]}</code> [link]</b>"
            )
        if link.startswith(("https", "t.me")):
            msg_id = int(link.split("/")[-1])
            if "t.me/c/" in link:
                chat = int("-100" + str(link.split("/")[-2]))
            else:
                chat = str(link.split("/")[-2])
            try:
                get_msg = await client.get_messages(chat, msg_id)
                try:
                    await get_msg.copy(message.chat.id)
                except Exception:
                    return await helpersdb.Tools.download_media(
                        get_msg, client, proses, message
                    )
            except Exception as er:
                return await message.reply(str(er))
        else:
            return await message.reply("Link tidak valid.")
    except Exception as er:
        logger.error(f"copy eror {str(er)}")


async def dne_plugins(client, message):
    data_module = await databasedb.dB.get_var(config.BOT_ID, "DISABLED_MODULES") or []
    if message.command[0] == "disable":
        if len(message.command) < 2:
            return await message.reply("**Please give name for disable**")
        name = message.text.split(None, 1)[1]
        if name.lower() in data_module:
            return await message.reply(f"**Command {name} already disabled**")
        data_module.append(name.lower())
        await databasedb.dB.set_var(config.BOT_ID, "DISABLED_MODULES", data_module)
        return await message.reply(f"**Disabled commands: `{name}`.**")
    elif message.command[0] == "enable":
        if len(message.command) < 2:
            return await message.reply("**Please give plugins name for enable**")
        name = message.text.split(None, 1)[1]
        if name.lower() not in data_module:
            return await message.reply(f"**Command {name} already enable**")
        data_module.remove(name.lower())
        await databasedb.dB.set_var(config.BOT_ID, "DISABLED_MODULES", data_module)
        return await message.reply(f"**Enabled commands: `{name}`.**")

    elif message.command[0] == "disabled":
        if len(data_module) == 0:
            return await message.reply(f"**You dont have disabled commands.**")
        msg = "**List disabled plugins:**\n\n"
        for count, name in enumerate(data_module, 1):
            msg += f"**{count}**. `{name}`\n"
        return await message.reply(msg)
