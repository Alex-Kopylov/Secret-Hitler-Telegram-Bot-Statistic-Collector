import os
from pathlib import Path
from typing import Literal, List, Tuple

from dotenv import load_dotenv

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
DEVELOPER_CHAT_ID = os.getenv("DEVELOPER_CHAT_ID", "")

# Database constants
SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", Path().resolve() / "database/db.sqlite")
DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

# Game constants
MAX_VOTES = 10
MAX_HITLER_VOTERS = 1
MIN_HITLER_VOTERS = 1
MAX_LIBERAL_VOTERS = 6
MIN_LIBERAL_VOTERS = 3
MAX_FASCIST_VOTERS = 3
MIN_FASCIST_VOTERS = 1

GAME_POLL_OUTCOMES: Tuple = (
    "I'm Canceler Hitler",
    "I'm Dead Hitler",
    "I'm Hitler Loser",
    "I'm Liberal Winner",
    "I'm Liberal Loser",
    "I'm Fascistic Winner",
    "I'm Fascistic Loser",
)
