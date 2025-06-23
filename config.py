import logging
import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# BACKEND = "Text"  # Errbot will start in text mode (console only mode) and will answer commands from there.
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


# Digest configuration
DIGEST_SEND_TIME = os.environ.get("DIGEST_SEND_TIME", "6:30")  # Default to 6:30 UTC

BOT_IDENTITY = {
    # Required
    "team": os.environ.get("ERRBOT_TEAM"),
    "server": os.environ.get("ERRBOT_SERVER"),
    "token": os.environ.get("ERRBOT_TOKEN"),
    # Optional
    # "insecure": False,  # Default = False. Set to true for self signed certificates
    "scheme": "https",  # Default = https
    "port": 443,  # Default = 8065
    "timeout": 30,  # Default = 30. If the web server disconnects idle connections later/earlier change this value
    # "cards_hook": "incomingWebhookId",  # Needed for cards/attachments
}
