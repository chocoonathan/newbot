import asyncio
import traceback

from pyrogram.errors import FloodPremiumWait, FloodWait, RPCError

from helpers import Emoji, Tools, animate_proses
from logs import logger


async def copyall_cmd(client, message):
    em = Emoji(client)
    await em.get()
    args = message.command[1:]

    if len(args) < 1:
        return await message.reply(
            f"**Please provide links**\nExample: `{message.text.split()[0]} https://t.me/c/2425084669/3746,https://t.me/c/2425084669/3748,https://t.me/c/2425084669/3749`"
        )

    proses = await animate_proses(message, em.proses)
    chat_id = message.chat.id
    links_input = args[0]

    links_list = [link.strip() for link in links_input.split(",")]

    successful_copies = 0
    skipped_messages = 0

    try:
        for link in links_list:
            chats, msg_id = Tools.get_link(link)
            if chats is None or msg_id is None:
                await message.reply(f"**Invalid link: {link}**")
                continue

            logger.info(f"Processing message {msg_id} from chat {chats}")

            try:
                msg = await client.get_messages(chats, msg_id)

                if not msg:
                    skipped_messages += 1
                    await message.reply(f"<b>Message not found: {link}</b>")
                    continue
                try:
                    await msg.copy(chat_id)
                    successful_copies += 1
                    logger.info(f"Successfully copied message {msg_id}")
                except (FloodWait, FloodPremiumWait) as wet:
                    await asyncio.sleep(wet.value)
                    await msg.copy(chat_id)
                    successful_copies += 1
                    logger.info(
                        f"Successfully copied message {msg_id} after flood wait"
                    )
                except Exception as copy_error:
                    if msg.media:
                        cnt = await message.reply(
                            f"<b>Can't copy media message {msg_id}, trying to download...</b>"
                        )
                        if await Tools.download_media(msg, client, cnt, message):
                            successful_copies += 1
                            logger.info(
                                f"Successfully downloaded media message {msg_id}"
                            )
                        else:
                            skipped_messages += 1
                            logger.error(
                                f"Failed to download media message {msg_id}: {copy_error}"
                            )
                    else:
                        try:
                            if msg.text:
                                await client.send_message(chat_id, msg.text)
                                successful_copies += 1
                                logger.info(f"Successfully sent text message {msg_id}")
                            else:
                                skipped_messages += 1
                                logger.error(
                                    f"Failed to process message {msg_id}: {copy_error}"
                                )
                        except Exception as text_error:
                            skipped_messages += 1
                            logger.error(
                                f"Failed to send text message {msg_id}: {text_error}"
                            )

            except (FloodWait, FloodPremiumWait) as flood:
                logger.error(f"FloodWait: Waiting for {flood.value} seconds")
                await asyncio.sleep(flood.value)
                try:
                    msg = await client.get_messages(chats, msg_id)
                    if msg:
                        await msg.copy(chat_id)
                        successful_copies += 1
                except Exception:
                    skipped_messages += 1
                    await message.reply(
                        f"<b>Failed to process after flood wait: {link}</b>"
                    )
            except RPCError as rpc_error:
                logger.error(f"RPC Error for message {msg_id}: {rpc_error}")
                skipped_messages += 1
                await message.reply(f"<b>RPC Error for: {link}</b>")
            except Exception as er:
                logger.error(
                    f"Error processing message {msg_id}: {traceback.format_exc()}"
                )
                skipped_messages += 1
                await message.reply(f"<b>Unexpected error for: {link}</b>")

        await proses.delete()
        return await message.reply(
            f"<b>Copying completed.\n"
            f"Total links processed: {len(links_list)}\n"
            f"Successfully copied: {successful_copies}\n"
            f"Skipped messages: {skipped_messages}</b>"
        )

    except Exception as e:
        logger.error(f"Overall process error: {traceback.format_exc()}")
        return await message.reply(f"An unexpected error occurred: {str(e)}")
