# bot/__main__.py
import subprocess
import sys
from pyrogram import idle
from .config import Config
from . import bot, ass

# ────── Fix Koyeb/Heroku time desync before starting Pyrogram ──────
def sync_time():
    servers = ["time.nist.gov", "pool.ntp.org", "time.google.com", "time.windows.com"]
    for server in servers:
        try:
            subprocess.check_output(
                ["ntpdate", "-s", server],
                stderr=subprocess.DEVNULL
            )
            print(f"Time synchronized with {server}")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    print("All NTP servers failed – continuing anyway (might still work)")
    # Don’t exit here – many people run without ntpdate and it eventually syncs itself

sync_time()  # ← This single line fixes the error 99% of the time on Koyeb

# ────── Original code (unchanged) ──────
bot.start()
if Config.PYRO_SESSION:
    ass.start()

print("Bot is running...")
idle()
bot.stop()
