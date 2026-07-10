import asyncio
import discord
from discord.ext import commands
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

    await bot.tree.sync()

    print("Commands synced")


async def main():

    await load_extensions()

    await bot.start(TOKEN)


asyncio.run(main())
