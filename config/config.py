import logging
import os

# BACKEND = "Text"  # Errbot will start in text mode (console only mode) and will answer commands from there.
BACKEND = "Mattermost"

BOT_DATA_DIR = r"./data"
BOT_EXTRA_PLUGIN_DIR = r"./plugins"
BOT_EXTRA_BACKEND_DIR = r"./backend-plugins"

BOT_LOG_FILE = r"./errbot.log"
BOT_LOG_LEVEL = logging.INFO

BOT_ADMINS = ["@jocave","mz2"]

BOT_IDENTITY = {
    # Required
    "team": os.environ.get("ERRBOT_TEAM", "Canonical"),
    "server": os.environ.get("ERRBOT_SERVER", "chat.canonical.com"),
    "token": os.environ.get("ERRBOT_TOKEN"),
    # Optional
    "insecure": False,  # Default = False. Set to true for self signed certificates
    "scheme": "https",  # Default = https
    "port": 443,  # Default = 8065
    "timeout": 30,  # Default = 30. If the web server disconnects idle connections later/earlier change this value
    # "cards_hook": "incomingWebhookId",  # Needed for cards/attachments
}
