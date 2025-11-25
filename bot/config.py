# bot/config.py
import os
from os import getenv

class Config:
    # Required: Bot token from @BotFather
    TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN", "").strip()

    # Optional: User session string (you don't use it → leave empty or False)
    PYRO_SESSION = getenv("PYRO_SESSION", "").strip() or False

    # Telegram API credentials (from my.telegram.org)
    TELEGRAM_APP_ID = getenv("TELEGRAM_APP_ID")
    TELEGRAM_APP_HASH = getenv("TELEGRAM_APP_HASH")

    # ────── Validation ──────
    if not TELEGRAM_APP_ID or not TELEGRAM_APP_ID.isdigit():
        raise ValueError("TELEGRAM_APP_ID is missing or invalid! Get it from https://my.telegram.org")

    if not TELEGRAM_APP_HASH:
        raise ValueError("TELEGRAM_APP_HASH is missing! Get it from https://my.telegram.org")

    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is missing! Get it from @BotFather")

    # Convert to int only after validation
    TELEGRAM_APP_ID = int(TELEGRAM_APP_ID)

    # Optional warning if someone accidentally sets PYRO_SESSION
    if PYRO_SESSION:
        print("[WARNING] PYRO_SESSION is set — user client will be started (not needed for banall bot)")
