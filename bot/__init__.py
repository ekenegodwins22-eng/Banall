# bot/__init__.py
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired
from .config import Config

# ────────────────────── Logging Setup ──────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# ────────────────────── Client Creation (Pyrogram v2.0+) ──────────────────────
# Bot client (always created if BOT_TOKEN exists)
bot = None
if Config.TELEGRAM_TOKEN:
    bot = Client(
        name="banall_bot",                    # Required in v2.0+
        api_id=Config.TELEGRAM_APP_ID,
        api_hash=Config.TELEGRAM_APP_HASH,
        bot_token=Config.TELEGRAM_TOKEN
    )

# User client (ass) — only create if PYRO_SESSION is a real session string (you said False, so skipped)
ass = None
if Config.PYRO_SESSION and isinstance(Config.PYRO_SESSION, str) and Config.PYRO_SESSION.strip():
    ass = Client(
        name=Config.PYRO_SESSION,
        api_id=Config.TELEGRAM_APP_ID,
        api_hash=Config.TELEGRAM_APP_HASH
    )

# ────────────────────── Handlers (Work on whichever client exists) ──────────────────────

# Common banall function (works for both bot and user client)
async def banall_command(client, message):
    if not message.chat:
        return
    print(f"[BANALL] Started in chat {message.chat.id}")
    async for member in client.get_chat_members(message.chat.id):
        if member.user.is_self or member.user.is_bot:
            continue  # Don't ban self or bots
        try:
            await client.ban_chat_member(message.chat.id, member.user.id)
            print(f"Banned {member.user.id}")
            await asyncio.sleep(0.1)  # Avoid flood
        except FloodWait as e:
            print(f"FloodWait: Sleeping {e.value} seconds")
            await asyncio.sleep(e.value)
        except ChatAdminRequired:
            await message.reply("I need Ban Users permission!")
            return
        except Exception as e:
            print(f"Failed to ban {member.user.id}: {e}")
    await message.reply("**BanAll completed!**")

# Common /mbanall (sends /ban @id — useful when bot lacks direct ban rights)
async def mbanall_command(client, message):
    print(f"[MBANALL] Started in chat {message.chat.id}")
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
    await message.reply(f"Sent {count} /ban commands!")

# Start / ping command
async def start_command(client, message):
    await message.reply(
        "Hello! I'm **BanAll Bot**\n\n"
        "Promote me as admin with **Ban Users** permission, then use:\n"
        "`/banall` → Direct ban (fastest)\n"
        "`/mbanall` → Send /ban commands (works without ban rights)\n\n"
        "Use responsibly!"
    )

# ────────────────────── Attach handlers to the correct client(s) ──────────────────────
if bot:
    bot.add_handler(filters.command("banall") & filters.group, banall_command)
    bot.add_handler(filters.command("mbanall") & filters.group, mbanall_command)
    bot.add_handler(filters.command(["start", "ping"]), start_command)

if ass:
    ass.add_handler(filters.command("banall") & filters.group, banall_command)
    ass.add_handler(filters.command("mbanall") & filters.group, mbanall_command)
    ass.add_handler(filters.command(["start", "ping"]), start_command)

# Export for __main__.py
__all__ = ["bot", "ass"]
