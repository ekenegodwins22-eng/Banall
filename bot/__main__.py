# bot/__main__.py
import os
import asyncio
from pyrogram import idle
from . import bot, ass

# ────── Tiny aiohttp health-check server (required for Koyeb HTTP health check) ──────
from aiohttp import web

async def health(request):
    return web.Response(text="BanAll Bot is alive and ready to destroy!")

app = web.Application()
app.router.add_get('/health', health)

async def web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Health server running on port {port} → /health")

# ────── Safe start with session cleanup + retry (your proven fix) ──────
async def safe_start(client):
    session_file = f"{client.name}.session"
    for attempt in range(1, 6):
        try:
            if os.path.exists(session_file):
                os.remove(session_file)
                print(f"Deleted stale session: {session_file}")
            await client.start()
            print(f"{client.name} connected successfully!")
            return
        except Exception as e:
            print(f"{client.name} attempt {attempt} failed: {e}")
            if attempt < 5:
                await asyncio.sleep(5 * attempt)
    raise RuntimeError(f"Failed to start {client.name} after 5 attempts")

# ────── Main ──────
async def main():
    tasks = [web_server(), safe_start(bot)]
    if ass:  # Only starts if PYRO_SESSION is set
        tasks.append(safe_start(ass))
    
    await asyncio.gather(*tasks)
    print("BanAll bot is now ONLINE and unstoppable!")
    await idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped gracefully.")
