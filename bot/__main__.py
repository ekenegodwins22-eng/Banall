# bot/__main__.py
import os
import time
import asyncio
from pyrogram import idle
from .config import Config
from . import bot, ass  # Keep 'ass' import even if unused

# ────── Enhanced time sync & retry for Koyeb/Heroku (no ntpdate needed) ──────
async def safe_start(client):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Delete stale session file to reset clock (Pyrogram v2.x handles regen safely)
            session_file = f"{client.name}.session"
            if os.path.exists(session_file):
                os.remove(session_file)
                print(f"Deleted stale session: {session_file} (forces fresh clock sync)")
            
            await client.start()
            print("Bot connected successfully!")
            return True
        except Exception as e:
            print(f"Connect attempt {attempt + 1}/{max_retries} failed: {e}")
            if "BadMsgNotification" in str(e) and attempt < max_retries - 1:
                # Wait & retry—gives Koyeb time to settle (v2.x recovers better)
                await asyncio.sleep(5 * (attempt + 1))  # Progressive backoff: 5s, 10s, 15s...
            else:
                raise  # Re-raise on final fail

# ────── Main startup ──────
async def main():
    await safe_start(bot)
    if Config.PYRO_SESSION:
        await safe_start(ass)  # Apply same logic if ever enabled
    
    print("BanAll bot is now running...")
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
