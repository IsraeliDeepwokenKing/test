import discord

from discord import app_commands
from discord.ext import commands


class Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup",
        description="Sets up carry system"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(
        self,
        interaction: discord.Interaction
    ):

        guild = interaction.guild

        await interaction.response.defer(
            ephemeral=True
        )

        category = discord.utils.get(
            guild.categories,
            name="Deepwoken Carry"
        )

        if category is None:

            category = await guild.create_category(
                "Deepwoken Carry"
            )

        channels = [

            "host-commands",

            "carry-pings",

            "incident-reports",

            "logs"

        ]

        for name in channels:

            channel = discord.utils.get(
                guild.text_channels,
                name=name
            )

            if channel:

                continue

            overwrites = {

                guild.default_role:
                discord.PermissionOverwrite(

                    view_channel=True,

                    send_messages=True

                )

            }

            # carry-pings

            if name == "carry-pings":

                overwrites[guild.default_role] = discord.PermissionOverwrite(

                    view_channel=True,

                    send_messages=False

                )

                overwrites[guild.me] = discord.PermissionOverwrite(

                    view_channel=True,

                    send_messages=True

                )

            # logs

            elif name == "logs":

                overwrites[guild.default_role] = discord.PermissionOverwrite(

                    view_channel=False

                )

                overwrites[guild.me] = discord.PermissionOverwrite(

                    view_channel=True,

                    send_messages=True

                )

            await guild.create_text_channel(

                name=name,

                category=category,

                overwrites=overwrites

            )

        roles = [

            "Titus Hoster",

            "Elder Hoster",

            "Enmity Hoster",

            "Titus Ping",

            "Elder Ping",

            "Enmity Ping"

        ]

        for role_name in roles:

            role = discord.utils.get(

                guild.roles,

                name=role_name

            )

            if role is None:

                await guild.create_role(

                    name=role_name,

                    mentionable=True,

                    reason="CarryBot setup"

                )

            else:

                if not role.mentionable:

                    await role.edit(

                        mentionable=True

                    )

        await interaction.followup.send(

            "Setup has finished.",

            ephemeral=True

        )


async def setup(bot):

    await bot.add_cog(

        Setup(bot)

    )
