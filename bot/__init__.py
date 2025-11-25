# bot/__init__.py
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired
from .config import Config

# ────────────────────── Logging Setup ──────────────────────
logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# ────────────────────── Client Creation (Pyrogram v2.0+) ──────────────────────
bot = Client(
    name="banall_bot",
    api_id=Config.TELEGRAM_APP_ID,
    api_hash=Config.TELEGRAM_APP_HASH,
    bot_token=Config.TELEGRAM_TOKEN
)

ass = None
if Config.PYRO_SESSION and isinstance(Config.PYRO_SESSION, str) and Config.PYRO_SESSION.strip():
    ass = Client(
        name=Config.PYRO_SESSION,
        api_id=Config.TELEGRAM_APP_ID,
        api_hash=Config.TELEGRAM_APP_HASH
    )

# ────────────────────── Command Functions ──────────────────────
async def start_command(client, message):
    await message.reply(
        "Hello! I'm **BanAll Bot**\n\n"
        "Promote me as admin with **Ban Users** permission, then use:\n"
        "`/banall` → Direct ban (fastest)\n"
        "`/mbanall` → Send /ban commands (works without ban rights)\n\n"
        "Use responsibly!"
    )

async def banall_command(client, message):
    print(f"[BANALL] Started in chat {message.chat.id}")
    await message.reply("**BanAll started…**")
    count = 0
    async for member in client.get_chat_members(message.chat.id):
        if member.user.is_self or member.user.is_bot or member.status in ("administrator", "creator"):
            continue
        try:
            await client.ban_chat_member(message.chat.id, member.user.id)
            count += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except ChatAdminRequired:
            await message.reply("I need **Ban Users** permission to do this!")
            return
        except Exception as e:
            print(f"Failed to ban {member.user.id}: {e}")
    await message.reply(f"**BanAll completed! Banned {count} users.**")

async def mbanall_command(client, message):
    print(f"[MBANALL] Started in chat {message.chat.id}")
    await message.reply("**mBanAll started…**")
    count = 0
    async for member in client.get_chat_members(message.chat.id):
        try:
            await client.send_message(message.chat.id, f"/ban {member.user.id}")
            count += 1
            await asyncio.sleep(0.2)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Failed: {e}")
    await message.reply(f"**Sent {count} /ban commands!**")

# ────────────────────── Register Handlers (Correct Pyrogram 2.0+ syntax) ──────────────────────
# For the main bot (always exists)
bot.on_message(filters.command(["start", "ping"]))(start_command)
bot.on_message(filters.command("banall") & filters.group)(banall_command)
bot.on_message(filters.command("mbanall") & filters.group)(mbanall_command)

# For user client (only if enabled)
if ass:
    ass.on_message(filters.command(["start", "ping"]))(start_command)
    ass.on_message(filters.command("banall") & filters.group)(banall_command)
    ass.on_message(filters.command("mbanall") & filters.group)(mbanall_command)

# Export for __main__.py
__all__ = ["bot", "ass"]
