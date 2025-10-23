from typing import Optional

from pytz import timezone

from clients import session
from config import BOT_ID, BOT_NAME, USENAME_OWNER
from database import dB
from logs import logger


def get_user_info(user_id: int):
    client = session.get_session(user_id)
    if client:
        return {
            "first_name": client.me.first_name,
            "last_name": client.me.last_name or "",
            "username": client.me.username or "",
        }
    return {"first_name": "User", "last_name": str(user_id), "username": ""}


class Message:
    """Enhanced message templates with modern formatting"""

    JAKARTA_TZ = timezone("Asia/Jakarta")

    # HTML formatting templates
    USER_MENTION = "<a href=tg://user?id={id}>{name}</a>"
    CODE_BLOCK = "<code>{text}</code>"
    SECTION_START = "<b>❏ {title}</b>"
    SECTION_ITEM = "<b>├ {label}:</b> {value}"
    SECTION_END = "<b>╰ {label}</b> {value}"

    @staticmethod
    def ReplyCheck(message):
        reply_id = None
        if message.reply_to_message:
            reply_id = message.reply_to_message.id
        elif not message.from_user:
            reply_id = message.id
        return reply_id

    @staticmethod
    async def _ads() -> str:
        txt = await dB.get_var(BOT_ID, "ads")
        if txt:
            msg = txt
        else:
            msg = f"Masih kosong, jika ingin promosi ads hubungi {USENAME_OWNER}"
        return msg

    @classmethod
    def _format_user_mention(
        cls, user_id: int, first_name: str, last_name: Optional[str] = None
    ) -> str:
        """Format user mention with full name"""
        full_name = f"{first_name} {last_name or ''}".strip()
        return cls.USER_MENTION.format(id=user_id, name=full_name)

    @classmethod
    def expired_message(cls, user_id: int) -> str:
        client = session.get_session(user_id)
        return f"""
{cls.SECTION_START.format(title="Notifikasi")}
{cls.SECTION_ITEM.format(
    label="Akun",
    value=cls._format_user_mention(client.me.id, client.me.first_name, client.me.last_name)
)}
{cls.SECTION_ITEM.format(label="ID", value=cls.CODE_BLOCK.format(text=client.me.id))}
{cls.SECTION_END.format(label="Status", value="Masa Aktif Telah Habis")}
"""

    @classmethod
    async def welcome_message(cls, client, message) -> str:
        """Generate personalized welcome message"""
        return f"""
<b>✨ Selamat datang, {cls._format_user_mention(
    message.from_user.id,
    message.from_user.first_name,
    message.from_user.last_name
)}!</b>

<b>🤖 Saya adalah <u>[{BOT_NAME}](https://t.me/{client.me.username})</u> asisten pintar yang akan membantu Anda membuat userbot dengan mudah dan cepat.
"""

    @staticmethod
    async def userbot_list(start_index=0):
        user_list = session.get_list()
        total_users = len(user_list)
        end_index = min(start_index + 10, total_users)

        message_text = "<b>📋 Daftar Userbot</b>\n\n"

        for i in range(start_index, end_index):
            user_id = user_list[i]
            try:
                user_info = get_user_info(user_id)
                account_name = (
                    f"{user_info['first_name']} {user_info['last_name'] or ''}"
                )
                message_text += (
                    f"<b>{i+1}.</b> {account_name} - <code>{user_id}</code>\n"
                )
            except Exception as e:
                message_text += f"<b>{i+1}.</b> Unknown - <code>{user_id}</code>\n"

        message_text += f"\n<b>Menampilkan {start_index + 1}-{end_index} dari {total_users} userbot</b>"

        return message_text

    @staticmethod
    async def userbot_detail(count: int):
        try:
            user_id = session.get_list()[count]
            user_info = get_user_info(user_id)
            client = session.get_session(user_id)
            v2l = await dB.get_var(user_id, "PASSWORD") or "-"
            expired_date = await dB.get_expired_date(user_id)
            expir = (
                expired_date.astimezone(timezone("Asia/Jakarta")).strftime(
                    "%Y-%m-%d %H:%M"
                )
                if expired_date
                else "-"
            )
            return f"""
<b>❏ Userbot ke </b> <code>{count + 1}/{session.get_count()}</code>
<b> ├ </b>
<b> ├ Akun:</b> <a href='tg://user?id={user_id}'>{user_info['first_name']} {user_info['last_name'] or ''}</a> 
<b> ├ ID:</b> <code>{user_id}</code>
<b> ├ No. Hp:</b> <code>{client.me.phone_number}</code>
<b> ├ Expired:</b> <code>{expir}</code>
<b> ╰ V2L:</b> <code>{v2l}</code> 
"""
        except Exception as e:
            logger.error(f"Error in userbot method: {e}")
            return f"<b>❌ Error: {e}</b>"

    @staticmethod
    async def userbot(count: int):
        try:
            user_id = session.get_list()[count]
            user_info = get_user_info(user_id)
            expired_date = await dB.get_expired_date(user_id)

            if expired_date:
                expir = expired_date.astimezone(timezone("Asia/Jakarta")).strftime(
                    "%Y-%m-%d %H:%M"
                )
            else:
                expir = "Unknown"

            return f"""
    <b>❏ Userbot ke </b> <code>{count + 1}/{session.get_count()}</code>
    <b> ├ Akun:</b> <a href='tg://user?id={user_id}'>{user_info['first_name']} {user_info['last_name'] or ''}</a> 
    <b> ├ ID:</b> <code>{user_id}</code>
    <b> ├ Username:</b> @{user_info['username'] or 'None'}
    <b> ╰ Expired:</b> <code>{expir}</code>
    """
        except Exception as e:
            logger.error(f"Error in userbot method: {e}")
            return f"<b>❌ Error: {e}</b>"

    @staticmethod
    def deak(X):
        return f"""
<b>Attention !!</b>
<b>Akun:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>ID:</b> <code>{X.me.id}</code>
<b>Reason:</b> <code>ᴅɪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴛᴇʟᴇɢʀᴀᴍ</code>
"""

    @staticmethod
    async def policy_message() -> str:
        """Generate enhanced policy and terms message"""
        return f"""
<b>🤖 {BOT_NAME} - Kebijakan & Ketentuan</b>

<b>💫 Kebijakan Pengembalian Dana</b>
• Anda memiliki hak pengembalian dana dalam 48 jam setelah pembelian
• Pengembalian hanya berlaku jika Anda belum menggunakan layanan
• Penggunaan fitur apapun menghilangkan hak pengembalian dana

<b>🛟 Dukungan Pelanggan</b>
• Panduan lengkap tersedia di bot ini
• Informasi risiko userbot: [Baca Di Sini](https://telegra.ph/RESIKO-USERBOT-08-09)
• Pembelian = Persetujuan terhadap semua risiko

<b>✅ Selanjutnya</b>
• Tekan 📃 <b>Saya Setuju</b> untuk melanjutkan pembelian
• Tekan 🏠 <b>Menu Utama</b> untuk kembali
"""

    @staticmethod
    def format_rupiah(angka):
        return f"Rp{angka:,}".replace(",", ".")

    @staticmethod
    def TEXT_PAYMENT(harga, total, bulan, plan, diskon=0):
        return f"""
<blockquote><b>Sebelum melanjutkan pembayaran silahkan pilih durasi terlebih dahulu.

Harga per bulan: <code>{Message.format_rupiah(harga)}</code>

🎁 Diskon: <code>{Message.format_rupiah(diskon)}</code>
🔖 Total harga: <code>{Message.format_rupiah(total)}</code>
🗓️ Masa aktif: <code>{bulan} bulan</code>
🛒 Plan: <code>{plan}</code>

🎉 Diskon tersedia jika membeli:
   • 2 bulan atau lebih: Rp10.000 (hingga 25%)
   • 5 bulan atau lebih: Rp25.000 (hingga 25%)
   • 12 bulan atau lebih: Rp80.000 (hingga 33%)

✅ Klik tombol Konfirmasi dibawah untuk melakukan pembayaran.</b></blockquote>
"""

    @staticmethod
    def chosePlan():
        return """
    **⚡ Plan Lite**
        <blockquote expandable>
        Akses ke sekitar 20 fitur dasar yang ringan dan cocok untuk pemula.
        Cek detail fiturnya di tombol ⚡ Plan Lite.
        Jumlah fitur bisa berubah sesuai pengembangan dari developer.
        </blockquote>

    **🧩 Plan Basic**
        <blockquote expandable>
        Nikmati akses ke sekitar 50 fitur unggulan yang memenuhi kebutuhan standar.
        Cek semua fiturnya di tombol 🧩 Plan Basic.
        Fitur bisa bertambah atau berkurang sesuai pengembangan dari developer.
        </blockquote>

    **💎 Plan Pro**
        <blockquote expandable>
        Unlock semua kemampuan dengan sekitar 90 fitur premium yang sangat lengkap!
        Lihat daftar fitur lengkapnya di tombol 💎 Plan Pro.
        Fitur akan terus dikembangkan dan bisa berubah sesuai keputusan developer.
        </blockquote>

    **Silahkan pilih plan sebelum melakukan pembayaran!**
    """
