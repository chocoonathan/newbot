import asyncio
import random
import traceback
from datetime import datetime

from pyrogram.errors import FloodPremiumWait, FloodWait, UserBannedInChannel

from clients import bot, session
from config import AUTOBC_STATUS, BLACKLIST_GCAST
from database import dB
from logs import logger

from .emoji_logs import Emoji


async def get_auto_gcast_messages(client):
    entries = await dB.get_var(client.me.id, "AUTO_GCAST") or []
    return [await client.get_messages("me", int(e["message_id"])) for e in entries]


async def safe_send_message(selected_msg, chat_id, watermark=None):
    thread_id = await dB.get_var(chat_id, "SELECTED_TOPIC") or None
    try:
        client = selected_msg._client

        if watermark:
            text = selected_msg.text
            caption = selected_msg.caption

            if text:
                await client.send_message(
                    chat_id, f"{text}\n\n{watermark}", message_thread_id=thread_id
                )
            elif caption:
                media_types = [
                    ("photo", selected_msg.photo),
                    ("video", selected_msg.video),
                    ("animation", selected_msg.animation),
                    ("audio", selected_msg.audio),
                    ("document", selected_msg.document),
                    ("sticker", selected_msg.sticker),
                ]

                file_id = None
                for media_type, media_obj in media_types:
                    if media_obj:
                        file_id = media_obj.file_id
                        break

                if file_id:
                    await client.send_cached_media(
                        chat_id,
                        file_id,
                        caption=f"{caption}\n\n{watermark}",
                        message_thread_id=thread_id,
                    )
            else:
                # Handle media tanpa caption
                media_types = [
                    ("photo", selected_msg.photo),
                    ("video", selected_msg.video),
                    ("animation", selected_msg.animation),
                    ("audio", selected_msg.audio),
                    ("document", selected_msg.document),
                    ("sticker", selected_msg.sticker),
                ]

                file_id = None
                for media_type, media_obj in media_types:
                    if media_obj:
                        file_id = media_obj.file_id
                        break

                if file_id:
                    await client.send_cached_media(
                        chat_id, file_id, caption=watermark, message_thread_id=thread_id
                    )
        else:
            await selected_msg.copy(chat_id, message_thread_id=thread_id)

        await asyncio.sleep(3)
        return {"status": "success"}

    except (FloodWait, FloodPremiumWait) as e:
        await asyncio.sleep(e.value)
        return await safe_send_message(selected_msg, chat_id, watermark)
    except UserBannedInChannel as e:
        return {"status": "banned", "error": str(e)}
    except Exception as e:
        return {"status": "failed", "error": f"{type(e).__name__}: {str(e)}"}


async def sending_message(client):
    try:
        messages = await get_auto_gcast_messages(client)
    except OSError:
        logger.error(f"Koneksi {client.me.id} putus")
        if client.me.id in AUTOBC_STATUS:
            AUTOBC_STATUS.remove(client.me.id)
        return
    if not messages:
        return
    while client.me.id in AUTOBC_STATUS:
        try:
            em = Emoji(client)
            await em.get()
            plan = await dB.get_var(client.me.id, "plan")
            watermark = None
            if plan != "is_pro":
                watermark = f"<blockquote><b>{em.robot}AutoBC by @{bot.username}</b></blockquote>"
            print(f"🔁 Running autobc for {client.me.id}")
            if not await dB.get_var(client.me.id, "DELAY_GCAST"):
                delay = 300
            else:
                delay = int(await dB.get_var(client.me.id, "DELAY_GCAST"))
            done = await dB.get_var(client.me.id, "ROUNDS") or 0
            group, failed = 0, 0
            blacklist = set(
                await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST") or []
            ) | set(BLACKLIST_GCAST)

            error_details = {}
            banned_count = 0

            selected_msg = random.choice(messages)
            chats = await client.get_chat_id("group")

            for chat_id in chats:
                if client.me.id not in AUTOBC_STATUS:
                    break
                if chat_id in blacklist:
                    continue
                result = await safe_send_message(selected_msg, chat_id, watermark)

                if isinstance(result, dict):
                    if result["status"] == "success":
                        group += 1
                    elif result["status"] == "banned":
                        failed += 1
                        banned_count += 1
                        error_type = "UserBannedInChannel"
                        error_details[error_type] = error_details.get(error_type, 0) + 1
                        # Stop autobc jika banned
                        await dB.remove_var(client.me.id, "AUTOBC")
                        if client.me.id in AUTOBC_STATUS:
                            AUTOBC_STATUS.remove(client.me.id)
                        await client.send_message(
                            "me",
                            f"**{em.warn}Your account has limited access**\n"
                            f"AutoBC has been disabled.\n"
                            f"Reason: {result.get('error', 'UserBannedInChannel')}",
                        )
                        break
                    elif result["status"] == "failed":
                        failed += 1
                        # Ekstrak tipe error
                        error_msg = result.get("error", "Unknown error")
                        error_type = (
                            error_msg.split(":")[0] if ":" in error_msg else error_msg
                        )
                        error_details[error_type] = error_details.get(error_type, 0) + 1

            done += 1
            await dB.set_var(client.me.id, "ROUNDS", done)
            await dB.set_var(client.me.id, "SUCCES_GROUP", group)
            await dB.set_var(client.me.id, "LAST_TIME", datetime.utcnow().timestamp())

            summary = (
                f"<b><i>{em.warn}Autobc Done\n"
                f"{em.sukses}Berhasil : {group} Chat\n"
                f"{em.gagal}Gagal : {failed} Chat\n"
            )

            if error_details:
                summary += f"\n{em.gagal}<b>Detail Error:</b>\n"
                for error_type, count in error_details.items():
                    summary += f"  • {error_type}: {count}x\n"

            summary += f"{em.msg}Putaran Ke {done} Delay {delay} detik</i></b>"

            try:
                await client.send_message("me", summary)
            except Exception:
                await dB.remove_var(client.me.id, "AUTOBC")
                if client.me.id in AUTOBC_STATUS:
                    AUTOBC_STATUS.remove(client.me.id)
            await asyncio.sleep(delay)
        except Exception:
            logger.error(traceback.format_exc())


async def AutoBC():
    logger.info("✅ AutoBC tasks started")
    while True:
        for user_id in session.get_list():
            client = session.get_session(user_id)
            if client:
                if (
                    await dB.get_var(client.me.id, "AUTOBC")
                    and client.me.id not in AUTOBC_STATUS
                ):
                    last_time = await dB.get_var(client.me.id, "LAST_TIME") or 0
                    if not await dB.get_var(client.me.id, "DELAY_GCAST"):
                        delay = 300
                    else:
                        delay = int(await dB.get_var(client.me.id, "DELAY_GCAST"))
                    now = datetime.utcnow().timestamp()

                    elapsed = now - last_time
                    if elapsed < delay:
                        continue

                    AUTOBC_STATUS.append(client.me.id)
                    asyncio.create_task(sending_message(client))
        await asyncio.sleep(10)
