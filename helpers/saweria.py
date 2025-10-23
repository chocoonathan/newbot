import random
from datetime import datetime
from typing import Dict

import pytz
import qrcode

from .tools import Tools


class SaweriaApi:
    def __init__(self, api_key: str):
        """
        Initialize Saweria API

        Args:
            api_key (str): Your Maelyn API key
            timezone (str): Timezone for datetime conversion (default: Asia/Jakarta)
        """
        self.api_key = api_key
        self.base_url = "https://api.maelyn.sbs/api/saweria"
        self.timezone = pytz.timezone("Asia/Jakarta")

    def random_sender(self) -> str:
        names = [
            "Budi",
            "Ani",
            "Dedi",
            "Rina",
            "Joko",
            "Siti",
            "Ahmad",
            "Dewi",
            "Agus",
            "Linda",
            "Rudi",
            "Maya",
            "Fajar",
            "Nina",
            "Hendra",
            "Lina",
            "Yanto",
            "Bayu",
            "Dina",
            "Rizky",
            "Sari",
            "Aji",
            "Rita",
            "Doni",
            "Wati",
            "Irfan",
            "Yuni",
            "Rama",
            "Dewi",
        ]
        return random.choice(names)

    async def get_user_id(self, username: str) -> Dict:
        """
        Get Saweria user ID by username

        Args:
            username (str): Saweria username

        Returns:
            Dict: API response
        """
        url = f"{self.base_url}/check/user"

        headers = {"Content-Type": "application/json", "mg-apikey": self.api_key}

        payload = {"username": username.strip()}

        try:
            response = await Tools.fetch.post(url, headers=headers, json=payload)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": f"Failed to get user ID: {str(e)}"}

    def to_crc16(self, data):
        """Calculate CRC16 for QRIS"""
        crc = 0xFFFF
        for byte in data.encode():
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0x8408
                else:
                    crc >>= 1
        crc ^= 0xFFFF
        return format(crc, "04X")

    def _generate_qris_image(self, qr_string: str, nominal: int, path: str) -> str:
        """
        Generate QRIS image from QR string with specified nominal

        Args:
            qr_string (str): Original QRIS string from payment API
            nominal (int): Payment amount
            path (str): Output path for QR code image

        Returns:
            str: Path to generated QR code image
        """
        qris_without_crc = qr_string[:-4]
        qris_dynamic = qris_without_crc.replace("010211", "010212")
        qris_parts = qris_dynamic.split("5802ID")
        nominal_str = str(nominal)
        amount_tag = f"54{str(len(nominal_str)).zfill(2)}{nominal_str}5802ID"
        qris_output = qris_parts[0] + amount_tag + qris_parts[1]
        crc16 = self.to_crc16(qris_output)
        qris_output += crc16
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(qris_output)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path)

        return path

    async def create_payment(
        self,
        user_id: str,
        amount: int,
        email: str,
        message: str = "",
        qris_path: str = None,
    ) -> Dict:
        """
        Create Saweria payment with QRIS generation

        Args:
            user_id (str): Saweria user ID
            amount (int): Payment amount
            name (str): Customer name
            email (str): Customer email
            message (str): Payment message
            qris_path (str): Path to save QRIS image (optional)

        Returns:
            Dict: {
                "status": "success/error",
                "message": "...",
                "data": {
                    "payment_id": "...",
                    "amount": int,
                    "amount_raw": int,
                    "qr_string": "...",
                    "qris_path": "...",
                    "expired_at": "...",
                    "expired_at_local": datetime object,
                    "created_at": datetime object
                }
            }
        """
        url = f"{self.base_url}/create/payment"

        headers = {"Content-Type": "application/json", "mg-apikey": self.api_key}

        payload = {
            "user_id": user_id.strip(),
            "amount": str(amount),
            "name": self.random_sender(),
            "email": email.strip(),
            "msg": message.strip(),
        }

        try:
            response = await Tools.fetch.post(
                url, headers=headers, json=payload, timeout=10
            )
            result = response.json()

            if response.status_code != 200 or not result.get("result"):
                return {
                    "status": "error",
                    "message": "Failed to create payment",
                    "data": None,
                }

            data = result["result"]["data"]
            payment_id = data["id"]
            amount_raw = data["amount_raw"]
            qr_string = data["qr_string"]
            expired_str = data["expired_at"]
            expired_naive = datetime.strptime(expired_str, "%d/%m/%Y %H:%M:%S")
            expired_utc = pytz.utc.localize(expired_naive)
            expired_local = expired_utc.astimezone(self.timezone)
            if qris_path is None:
                qris_path = f"qris_{payment_id}_{amount_raw}.png"
            self._generate_qris_image(qr_string, amount_raw, qris_path)

            return {
                "status": "success",
                "message": "Payment created successfully",
                "data": {
                    "payment_id": payment_id,
                    "amount": amount,
                    "amount_raw": amount_raw,
                    "qr_string": qr_string,
                    "qris_path": qris_path,
                    "expired_at": expired_str,
                    "expired_at_local": expired_local,
                    "created_at": datetime.now(self.timezone),
                },
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create payment: {str(e)}",
                "data": None,
            }

    async def check_payment(self, user_id: str, payment_id: str) -> Dict:
        """
        Check Saweria payment status

        Args:
            user_id (str): Saweria user ID
            payment_id (str): Payment ID

        Returns:
            Dict: API response
        """
        url = f"{self.base_url}/check/payment"

        headers = {"Content-Type": "application/json", "mg-apikey": self.api_key}

        payload = {"user_id": user_id.strip(), "payment_id": payment_id.strip()}

        try:
            response = await Tools.fetch.post(
                url, headers=headers, json=payload, timeout=10
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": f"Failed to check payment: {str(e)}"}

    @staticmethod
    def format_rupiah(amount: int) -> str:
        """
        Format amount to Rupiah currency

        Args:
            amount (int): Amount to format

        Returns:
            str: Formatted rupiah string (e.g., "Rp 10.000")
        """
        return f"Rp {amount:,}".replace(",", ".")
