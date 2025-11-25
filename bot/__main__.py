# bot/__init__.py
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired
from .config import Config

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# ────── Clients ──────
bot = Client(
    name="banall_bot",
    api_id=Config.TELEGRAM_APP_ID,
    api_hash=Config.TELEGRAM_APP_HASH,
    bot_token=Config.TELEGRAM_TOKEN
) if Config.TELEGRAM_TOKEN else None

ass = None
if Config.PYRO_SESSION and isinstance(Config.PYRO_SESSION, str) and Config.PYRO_SESSION.strip():
    ass = Client(name=Config.PYRO_SESSION, api_id=Config.TELEGRAM_APP_ID, api_hash=Config.TELEGRAM_APP_HASH)

# ────── Command handlers (Pyrogram 2.0+ style) ──────
@bot.on_message(filters.command(["start", "ping"]))
async def start_cmd(client, message):
    await message.reply(
        "Hello! I'm **BanAll Bot**\n\n"
        "Promote me as admin with **Ban Users** permission, then use:\n"
        "`/banall` → Direct ban (fastest)\n"
        "`/mbanall` → Send /ban commands\n\n"
        "Use responsibly!"
    )

@bot.on_message(filters.command("banall") & filters.group)
async def banall_cmd(client, message):
    if not message.from_user:
        return
    await message.reply("**BanAll started…**")
    count = 0
    async for member in client.get_chat_members(message.chat.id):
        if member.status in ("administrator", "creator") or member.user.is_self:
            continue
        try:
            await client.ban_chat_member(message.chat.id, member.user.id)
            count += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            pass
    await message.reply(f"**BanAll completed! Banned {count} users.**")

@bot.on_message(filters.command("mbanall") & filters.group)
async def mbanall_cmd(client, message):
    await message.reply("**mBanAll started…**")
    count = 0
    async for member in client.get_chat_members(message.chat.id):
        try:
            await client.send_message(message.chat.id, f"/ban {member.user.id}")
            count += 1
            await asyncio.sleep(0.2)
        except FloodWait as e:
            await asyncio.sleep(e.value)
    await message.reply(f"**Sent {count} /ban commands!**")

# Optional: same handlers for ass (user client) — only if you ever enable PYRO_SESSION
if ass:
    ass.add_handler(filters.command(["start", "ping"]), start_cmd)
    ass.add_handler(filters.command("banall") & filters.group, banall_cmd)
    ass.add_handler(filters.command("mbanall") & filters.group, mbanall_cmd)

__all__ = ["bot", "ass"]
