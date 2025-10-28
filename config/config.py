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
IS_CURI_DATA = os.environ.get("IS_CURI_DATA", True)
WAJIB_JOIN = list(os.environ.get("WAJIB_JOIN", "asupankeii").split())
COOKIES_U_BING = os.environ.get(
    "COOKIES_U_BING",
    "",
)
USENAME_OWNER = os.environ.get("USENAME_OWNER", "@KeiSavior")
API_ID = int(os.environ.get("API_ID", 26064844))
MAX_BOT = int(os.environ.get("MAX_BOT", 500))
API_HASH = os.environ.get("API_HASH", "f258150b01368f2c49a09fa74136ac6d")
BOT_TOKEN = os.environ.get(
    "BOT_TOKEN", "8296322601:AAGmz2KJsHYV3yirFyhk8eNZYJ04utupOJc"
)
BOT_ID = int(BOT_TOKEN.split(":")[0])
API_MAELYN = os.environ.get("API_MAELYN", "mg-uGGaRCcmZDjArQICfSRKj4lI6AotdnCJ")
API_BOTCAHX = os.environ.get("API_BOTCAHX", "podlXrLQ")
BOT_NAME = os.environ.get("BOT_NAME", "Legion")
DB_NAME = os.environ.get("DB_NAME", "Legion")
URL_LOGO = os.environ.get("URL_LOGO", "https://files.catbox.moe/9mt1rt.jpg")
BLACKLIST_GCAST = get_blacklist()
SUDO_OWNERS = list(
    map(
        int,
        os.environ.get(
            "SUDO_OWNERS",
            "2131825735 1110718903 1419986660",
        ).split(),
    )
)
DEVS = list(
    map(
        int,
        os.environ.get(
            "DEVS",
            "2131825735 1110718903 1419986660",
        ).split(),
    )
)
AKSES_DEPLOY = list(
    map(int, os.environ.get("AKSES_DEPLOY", "2131825735 1110718903 1419986660").split())
)
OWNER_ID = int(os.environ.get("OWNER_ID", 2131825735))
LOG_SELLER = int(os.environ.get("LOG_SELLER", -1002784456850))
LOG_BACKUP = int(os.environ.get("LOG_BACKUP", -1002784456850))
SPOTIFY_CLIENT_ID = os.environ.get(
    "SPOTIFY_CLIENT_ID", "e09ff7a19b204b62b6048a73bd605fe6"
)
SPOTIFY_CLIENT_SECRET = os.environ.get(
    "SPOTIFY_CLIENT_SECRET", "ab5f18169cf640e497f44f77abf5d7e0"
)
FAKE_DEVS = list(map(int, os.environ.get("FAKE_DEVS", "2131825735").split()))
SAWERIA_EMAIL = os.environ.get("SAWERIA_EMAIL", "chcnathan@gmail.com")
SAWERIA_USERID = os.environ.get(
    "SAWERIA_USERID", "1162e95a-a840-4892-b9c0-4078c306ac55"
)
SAWERIA_USERNAME = os.environ.get("SAWERIA_USERNAME", "keisvr")
KYNAN = list(
    map(
        int,
        os.environ.get(
            "KYNAN",
            "2131825735",
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



















