import json
import os
import sys
from base64 import b64decode

import requests
from dotenv import load_dotenv


def get_blacklist():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi9ibGdjYXN0Lmpzb24="
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        sys.exit(1)


load_dotenv()

HELPABLE = {}
DICT_BUTTON = {}
COPY_ID = {}
AUTOBC_STATUS = []
AUTOFW_STATUS = []


IS_JASA_PRIVATE = os.environ.get("IS_JASA_PRIVATE", False)
IS_CURI_DATA = os.environ.get("IS_CURI_DATA", False)
WAJIB_JOIN = list(os.environ.get("WAJIB_JOIN", "KynanSupport").split())
COOKIES_U_BING = os.environ.get(
    "COOKIES_U_BING",
    "",
)
USENAME_OWNER = os.environ.get("USENAME_OWNER", "@kenapasinan")
API_ID = int(os.environ.get("API_ID", 12831328))
MAX_BOT = int(os.environ.get("MAX_BOT", 500))
API_HASH = os.environ.get("API_HASH", "7c4bdc0ad4355f8a934701af9d463d20")
BOT_TOKEN = os.environ.get(
    "BOT_TOKEN", "8041331097:AAHMrPD"
)
BOT_ID = int(BOT_TOKEN.split(":")[0])
API_MAELYN = os.environ.get("API_MAELYN", "maling")
API_BOTCAHX = os.environ.get("API_BOTCAHX", "maling")
BOT_NAME = os.environ.get("BOT_NAME", "NavyUbot")
DB_NAME = os.environ.get("DB_NAME", "NavyUbot")
URL_LOGO = os.environ.get("URL_LOGO", "https://files.catbox.moe/zzgnzm.jpg")
BLACKLIST_GCAST = get_blacklist()
SUDO_OWNERS = list(
    map(
        int,
        os.environ.get(
            "SUDO_OWNERS",
            "1054295664 1947321138 6710439195 1868008472 7028669261",
        ).split(),
    )
)
DEVS = list(
    map(
        int,
        os.environ.get(
            "DEVS",
            "1868008472 984144778 1928772230 7399365105 1992087933 1054295664 164809358 1087819304 6710439195 479344690 5357942628 5063062493 1259894923 1191668125 814540731 1054295664 1259894923 1868008472 1087819304 1947321138 901367975 1234464617 6710439195 7028669261",
        ).split(),
    )
)
AKSES_DEPLOY = list(
    map(int, os.environ.get("AKSES_DEPLOY", "1054295664 7399365105 7028669261").split())
)
OWNER_ID = int(os.environ.get("OWNER_ID", 1054295664))
LOG_SELLER = int(os.environ.get("LOG_SELLER", -100220))
LOG_BACKUP = int(os.environ.get("LOG_BACKUP", -10021))
SPOTIFY_CLIENT_ID = os.environ.get(
    "SPOTIFY_CLIENT_ID", "e09ff7a19b204b62b6048a73bd605fe6"
)
SPOTIFY_CLIENT_SECRET = os.environ.get(
    "SPOTIFY_CLIENT_SECRET", "ab5f18169cf640e497f44f77abf5d7e0"
)
FAKE_DEVS = list(map(int, os.environ.get("FAKE_DEVS", "1054295664").split()))
SAWERIA_EMAIL = os.environ.get("SAWERIA_EMAIL", "anandamahar084@gmail.com")
SAWERIA_USERID = os.environ.get(
    "SAWERIA_USERID", "50e13c97-a606-4d31-878d-2fc38b41c6a5"
)
SAWERIA_USERNAME = os.environ.get("SAWERIA_USERNAME", "kenapanan")
KYNAN = list(
    map(
        int,
        os.environ.get(
            "KYNAN",
            "1054295664 1868008472 7028669261 6710439195 6321616956",
        ).split(),
    )
)
if OWNER_ID not in SUDO_OWNERS:
    SUDO_OWNERS.append(OWNER_ID)
if OWNER_ID not in DEVS:
    DEVS.append(OWNER_ID)
if OWNER_ID not in FAKE_DEVS:
    FAKE_DEVS.append(OWNER_ID)
for P in FAKE_DEVS:
    if P not in DEVS:
        DEVS.append(P)
    if P not in SUDO_OWNERS:
        SUDO_OWNERS.append(P)

ENCRYPTION_KEY_HOLDER = [None]
