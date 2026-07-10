import asyncio
import discord
from discord.ext import commands
from aiohttp import web

from config import TOKEN


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


async def load_extensions():

    await bot.load_extension(
        "commands.setup"
    )

    await bot.load_extension(
        "commands.host"
    )


@bot.event
async def on_ready():

    print(f"Bot online: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")

    except Exception as e:
        print(e)



# Render web server

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

    runner = web.AppRunner(app)

    await runner.setup()


    port = 10000

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(
        f"Web server running on {port}"
    )



async def main():

    await load_extensions()

    await start_web_server()

    await bot.start(TOKEN)



asyncio.run(main())
