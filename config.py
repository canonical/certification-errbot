import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

BACKEND = "Mattermost"

BOT_DATA_DIR = r"./data"
BOT_EXTRA_PLUGIN_DIR = r"./plugins"

py_major_minor = f"{sys.version_info.major}.{sys.version_info.minor}"
BOT_EXTRA_BACKEND_DIR = (
    f".venv/lib/python{py_major_minor}/site-packages/err-backend-mattermost"
)

BOT_LOG_FILE = r"./errbot.log"
BOT_LOG_LEVEL = logging.DEBUG

if "ERRBOT_ADMINS" not in os.environ:
    raise ValueError("ERRBOT_ADMINS is not set")
BOT_ADMINS = os.environ.get("ERRBOT_ADMINS", "").split(",")


BOT_PREFIX = os.environ.get("BOT_PREFIX", "!")

DIGEST_SEND_TIME = os.environ.get("DIGEST_SEND_TIME", "6:30")

BOT_IDENTITY = {
    "team": os.environ.get("ERRBOT_TEAM"),
    "server": os.environ.get("ERRBOT_SERVER"),
    "token": os.environ.get("ERRBOT_TOKEN"),
    "scheme": "https",
    "port": 443,
    "timeout": 30,
}
