import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "")
QUIQ_API_TOKEN = os.getenv("QUIQ_API_TOKEN", "")

if ADMIN_CHAT_ID:
    try:
        ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)
    except ValueError:
        ADMIN_CHAT_ID = None

# В контейнере база лежит на примонтированном томе, поэтому путь настраивается.
DB_PATH = Path(os.getenv("DB_PATH") or BASE_DIR / "database.db")
BRANCHES_PATH = BASE_DIR / "data" / "branches.json"
CURRENCIES_PATH = BASE_DIR / "data" / "currencies.json"

ALERT_CHECK_INTERVAL_MINUTES = int(os.getenv("ALERT_CHECK_INTERVAL_MINUTES", "5"))
