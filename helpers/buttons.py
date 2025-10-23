import asyncio
import re
from math import ceil
from typing import List, Optional, Tuple
from uuid import uuid4

from pyrogram.errors import QueryIdInvalid, RPCError
from pyrogram.helpers import ikb, kb
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from clients import session
from database import dB, state
from logs import logger

COLUMN_SIZE = 4  # Controls the button number of height
NUM_COLUMNS = 2  # Controls the button number of width


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_categories(page_n, module_dict, prefix):
    categories = sorted(
        set([data.get("category", "Uncategorized") for data in module_dict.values()])
    )

    buttons = [
        EqInlineKeyboardButton(
            cat,
            callback_data=f"{prefix}_category({cat},{page_n})",
        )
        for cat in categories
    ]

    pairs = [buttons[i : i + NUM_COLUMNS] for i in range(0, len(buttons), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "⬅️",
                    callback_data=f"{prefix}_catprev({modulo_page})",
                ),
                EqInlineKeyboardButton(
                    "➡️",
                    callback_data=f"{prefix}_catnext({modulo_page})",
                ),
            )
        ]
    return pairs


def paginate_modules(page_n, module_dict, prefix, is_bot=False, category=None):
    modules = sorted(
        [
            EqInlineKeyboardButton(
                x["module"].__MODULES__,
                callback_data="{}_module({},{},{})".format(
                    prefix,
                    x["module"].__MODULES__.lower(),
                    page_n,
                    category if category else "all",
                ),
            )
            for x in module_dict.values()
            if hasattr(x["module"], "__MODULES__")
        ]
    )
    pairs = [modules[i : i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    nav_buttons = []
    if len(pairs) > COLUMN_SIZE:
        nav_buttons = [
            (
                EqInlineKeyboardButton(
                    "⬅️",
                    callback_data="{}_prev({},{})".format(
                        prefix,
                        modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                        category if category else "all",
                    ),
                ),
                EqInlineKeyboardButton(
                    "➡️",
                    callback_data="{}_next({},{})".format(
                        prefix, modulo_page + 1, category if category else "all"
                    ),
                ),
            )
        ]

    back_button = []
    if category:
        back_button = [
            [
                EqInlineKeyboardButton(
                    "🔙 Back Category",
                    callback_data=f"{prefix}_backcat({page_n})",
                )
            ]
        ]
    else:
        back_button = [
            [
                EqInlineKeyboardButton(
                    "🔙 Back",
                    callback_data=f"{prefix}_help_back({page_n})",
                )
            ]
        ]

    if len(pairs) > COLUMN_SIZE:
        pairs = (
            pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)]
            + nav_buttons
            + back_button
        )
    else:
        pairs = pairs + back_button

    return pairs


async def auto_delete_message(client, chat_id, message_id, delay=300):
    try:
        await asyncio.sleep(delay)
        await dB.remove_var(chat_id, "is_bot_pro")
        await dB.remove_var(chat_id, "is_bot")
        await dB.remove_var(chat_id, "is_bot_basic")
        await client.delete_messages(chat_id, message_id)
    except Exception:
        pass


class ButtonUtils:
    # Compile regex patterns for better performance
    URL_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?|tg://\S+"
    )
    BUTTON_PATTERN = re.compile(r"\[(.*?)\|(.*?)\]")
    FORMAT_TAGS = {
        "<b>": "**",
        "<i>": "__",
        "<strike>": "~~",
        "<spoiler>": "||",
        "<u>": "--",
    }

    @staticmethod
    def is_url(text: str) -> bool:
        """Check if text is a URL."""
        # return bool(ButtonUtils.URL_PATTERN.match(text))
        return bool(re.search(ButtonUtils.URL_PATTERN, text))

    @staticmethod
    def is_number(text: str) -> bool:
        """Check if text is a number."""
        return text.isdigit()

    @staticmethod
    def is_copy(text: str) -> bool:
        pattern = r"copy:"

        return bool(re.search(pattern, text))

    @staticmethod
    def is_alert(text: str) -> bool:
        pattern = r"alert:"

        return bool(re.search(pattern, text))

    @staticmethod
    def is_web(text: str) -> bool:
        pattern = r"web:"

        return bool(re.search(pattern, text))

    @staticmethod
    def cek_tg(text):
        tg_pattern = r"https?:\/\/files\.catbox\.moe\/\S+"
        match = re.search(tg_pattern, text)

        if match:
            tg_link = match.group(0)
            non_tg_text = text.replace(tg_link, "").strip()
            return tg_link, non_tg_text
        else:
            return (None, text)

    @staticmethod
    def parse_msg_buttons(texts: str) -> Tuple[str, List[List]]:
        btn = []
        for z in ButtonUtils.BUTTON_PATTERN.findall(texts):
            text, url = z
            urls = url.split("|")
            url = urls[0]
            if len(urls) > 1:
                btn[-1].append([text, url])
            else:
                btn.append([[text, url]])

        txt = texts
        for z in re.findall(r"\[.+?\|.+?\]", texts):
            txt = txt.replace(z, "")

        return txt.strip(), btn

    @staticmethod
    async def create_button(
        text: str, data: str, with_suffix: str = ""
    ) -> InlineKeyboardButton:
        """Create an InlineKeyboardButton based on data type."""
        data = data.strip()
        if ButtonUtils.is_url(data):
            return InlineKeyboardButton(text=text, url=data)
        elif ButtonUtils.is_number(data):
            return InlineKeyboardButton(text=text, user_id=int(data))
        elif ButtonUtils.is_copy(data):
            return InlineKeyboardButton(text=text, copy_text=data.replace("copy:", ""))
        elif ButtonUtils.is_alert(data):
            alert_text = data.replace("alert:", "")
            uniq = str(uuid4().int)[:8]
            await dB.set_var(int(uniq), int(uniq), alert_text)
            cb_data = f"alertcb_{int(uniq)}"
            return InlineKeyboardButton(text=text, callback_data=cb_data)
        return InlineKeyboardButton(
            text=text, callback_data=f"{data}_{with_suffix}" if with_suffix else data
        )

    @staticmethod
    async def create_inline_keyboard(
        buttons: List[List], suffix: str = ""
    ) -> InlineKeyboardMarkup:
        """Create InlineKeyboardMarkup from button data."""
        keyboard = []
        for row in buttons:
            if len(row) > 1:
                keyboard.append(
                    [
                        await ButtonUtils.create_button(text, data, suffix)
                        for text, data in row
                    ]
                )
            else:
                text, data = row[0]
                keyboard.append([await ButtonUtils.create_button(text, data, suffix)])
        return InlineKeyboardMarkup(keyboard)

    """Pre-defined keyboard templates for Pyrogram."""

    @staticmethod
    def start_menu(user_id: int) -> kb:
        """Generate start menu keyboard."""
        if not session.get_session(user_id):
            common_buttons = [
                ["✨ Mulai Buat Userbot"],
                ["❓ Status Akun"],
                [("⚡ Plan Lite"), ("🧩 Plan Basic"), ("💎 Plan Pro")],
                ["💬 Hubungi Admins"],
                ["🔑 Token"],
            ]
        else:
            common_buttons = [
                ["❓ Status Akun"],
                ["🔑 Token"],
                [
                    ("🔄 Reset Emoji"),
                    ("🔄 Reset Prefix"),
                ],
                [
                    ("🔄 Restart Userbot"),
                    ("🔄 Reset Text"),
                ],
                ["💬 Hubungi Admins"],
            ]
        return kb(common_buttons, resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def userbot_list(user_id, count, total_count):
        buttons = []

        nav_buttons = []
        if count > 0:
            nav_buttons.append(
                InlineKeyboardButton("❮", callback_data=f"prev_ub {count}")
            )

        page_number = (count // 10) * 10
        nav_buttons.append(
            InlineKeyboardButton("Kembali", callback_data=f"bcpg_acc {page_number}")
        )

        if count < total_count - 1:
            nav_buttons.append(
                InlineKeyboardButton("❯", callback_data=f"next_ub {count}")
            )

        buttons.append(nav_buttons)

        action_buttons = [
            [
                InlineKeyboardButton("Get OTP", callback_data=f"get_otp {count}"),
            ],
            [
                InlineKeyboardButton("Hapus User", callback_data=f"del_ubot {user_id}"),
                InlineKeyboardButton("Hapus Akun", callback_data=f"ub_deak {count}"),
            ],
        ]
        buttons.extend(action_buttons)

        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def account_list(start_index=0):
        user_list = session.get_list()
        total_users = len(user_list)

        buttons = []
        row = []
        end_index = min(start_index + 10, total_users)

        for i in range(start_index, end_index):
            user_id = user_list[i]
            button = InlineKeyboardButton(
                f"{i+1}", callback_data=f"tools_acc {user_id}-{i}"
            )
            row.append(button)

            if len(row) == 5:
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)

        nav_buttons = []

        if start_index > 0:
            nav_buttons.append(
                InlineKeyboardButton(
                    "◀️ Prev page", callback_data=f"acc_page {start_index - 10}"
                )
            )

        if end_index < total_users:
            nav_buttons.append(
                InlineKeyboardButton(
                    "Next page ▶️", callback_data=f"acc_page {end_index}"
                )
            )

        if nav_buttons:
            buttons.append(nav_buttons)

        buttons.append([InlineKeyboardButton("Tutup", callback_data="buttonclose")])

        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def deak(user_id, count):
        button = ikb(
            [[("⬅️", f"prev_ub {int(count)}"), ("Approve", f"deak_akun {int(count)}")]]
        )
        return button

    @staticmethod
    async def generate_inline_query(message, chat_id, bot_username, query):
        try:
            client = message._client
            results = await client.get_inline_bot_results(bot_username, query)
            if results and results.results:
                return {
                    "query_id": results.query_id,
                    "result_id": results.results[0].id,
                    "results": results.results,
                    "query": query,
                }
            return None
        except Exception:
            return None

    @staticmethod
    async def send_inline_bot_result(
        message,
        chat_id,
        bot_username,
        query,
        reply_to_message_id: Optional[int] = None,
    ) -> bool:
        client = message._client
        try:
            query_results = await ButtonUtils.generate_inline_query(
                message, chat_id, bot_username, query
            )

            if not query_results:
                return False

            data = await client.send_inline_bot_result(
                chat_id,
                query_results["query_id"],
                query_results["result_id"],
                reply_to_message_id=reply_to_message_id,
                message_thread_id=message.message_thread_id or None,
            )
            inline_id = {
                "chat": chat_id,
                "_id": data.updates[0].id,
                "me": client.me.id,
                "idm": id(message),
            }
            state.set(query, query, inline_id)
            if query not in ["inline_send", "pmpermit_inline", "inline_cancel"]:
                asyncio.create_task(
                    auto_delete_message(client, chat_id, data.updates[0].id, delay=120)
                )
            logger.info(f"Inline query '{query}'")
            return True
        except RPCError:
            raise
        except QueryIdInvalid:
            raise
        except Exception:
            raise

    @staticmethod
    def build_buttons(data, uniq, callback, closed):
        buttons = []
        row = []
        for idx, _ in enumerate(data):
            row.append((str(idx + 1), f"{callback}{idx}_{uniq}"))
            if len(row) == 5:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([("❌ Close", f"close {closed} {uniq}")])
        return ikb(buttons)

    @staticmethod
    def plus_minus(bulan, harga, plan):
        button = ikb(
            [
                [
                    ("⁻1 bulan", f"kurang {bulan} {harga} {plan}"),
                    ("⁺1 bulan", f"tambah {bulan} {harga} {plan}"),
                ],
                [("Konfirmasi", f"confirm {bulan} {harga} {plan}")],
                [("Batal", "buttonclose")],
            ]
        )
        return button

    @staticmethod
    def chose_plan():
        button = ikb(
            [
                [
                    ("🧩 Plan Basic", f"planusers basic"),
                    ("💎 Plan Pro", f"planusers is_pro"),
                ],
                [("⚡ Plan Lite", f"planusers lite")],
                [("Batal", "buttonclose")],
            ]
        )
        return button

    @staticmethod
    def create_font_keyboard(font_list, get_id, current_batch):
        keyboard = []
        for font_dict in font_list:
            for key, value in font_dict.items():
                keyboard.append(
                    InlineKeyboardButton(
                        key, callback_data=f"get_font {get_id} {value}"
                    )
                )

        rows = [keyboard[i : i + 2] for i in range(0, len(keyboard), 2)]

        while len(rows) < 3:
            rows.append([])

        rows.append(
            [
                InlineKeyboardButton(
                    "⬅️", callback_data=f"prev_font {get_id} {current_batch}"
                ),
                InlineKeyboardButton(
                    "➡️", callback_data=f"next_font {get_id} {current_batch}"
                ),
            ]
        )
        return rows
