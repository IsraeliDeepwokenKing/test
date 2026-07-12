import asyncio
import os

import discord
from aiohttp import web
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()

intents.members = True
intents.guilds = True
intents.message_content = True



bot = commands.Bot(
    command_prefix="!",
    intents=intents
)



# =====================
# LOAD COMMANDS
# =====================

async def load_extensions():

    extensions = [
        "commands.setup",
        "commands.host",
        "commands.endcarry"
    ]

    import traceback

    for extension in extensions:

        try:
            await bot.load_extension(extension)
            print(f"✅ Loaded {extension}")

        except Exception:
            print(f"\n❌ FAILED TO LOAD: {extension}")
            traceback.print_exc()


# =====================
# DISCORD EVENTS
# =====================


@bot.event
async def on_ready():

    print(
        f"Bot online: {bot.user}"
    )


    try:

        synced = await bot.tree.sync()

        print(
            f"Synced {len(synced)} slash commands"
        )


    except Exception as e:

        print(
            f"Command sync error: {e}"
        )



# =====================
# RENDER WEB SERVER
# =====================


async def health(request):

    return web.Response(

        text="Deepwoken Carry Bot Online"

    )




async def start_web_server():

    app = web.Application()


    app.router.add_get(
        "/",
        health
    )


    runner = web.AppRunner(
        app
    )


    await runner.setup()



    site = web.TCPSite(

        runner,

        "0.0.0.0",

        10000

    )


    await site.start()


    print(
        "Web server running on port 10000"
    )





# =====================
# MAIN
# =====================


async def main():

    await load_extensions()


    await start_web_server()


    await bot.start(
        TOKEN
    )





asyncio.run(main())
