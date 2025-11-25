# bot/__main__.py
import os
import asyncio
from pyrogram import idle
from . import bot, ass

# Tiny health-check web server for Koyeb
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
    print(f"Health server running → http://0.0.0.0:{port}/health")

# Safe start with session cleanup + retry (your original logic, kept because it’s solid)
async def safe_start(client):
    max_retries = 5
    session_file = f"{client.name}.session"
    for attempt in range(1, max_retries + 1):
        try:
            if os.path.exists(session_file):
                os.remove(session_file)
                print(f"Deleted stale session: {session_file}")
            await client.start()
            print(f"{client.name} connected successfully!")
            return
        except Exception as e:
            print(f"{client.name} attempt {attempt} failed: {e}")
            if attempt < max_retries:
                await asyncio.sleep(5 * attempt)
    raise RuntimeError(f"Failed to start {client.name} after {max_retries} attempts")

# Main entry point
async def main():
    # Start web server + bot(s) in parallel
    tasks = [web_server(), safe_start(bot)]
    if ass:  # ass is None if PYRO_SESSION disabled
        tasks.append(safe_start(ass))
    
    await asyncio.gather(*tasks)
    
    print("BanAll bot is now ONLINE and unstoppable!")
    await idle()  # Keeps everything alive forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("BanAll bot stopped gracefully.")
