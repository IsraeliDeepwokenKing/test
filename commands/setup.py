import discord
from discord import app_commands
from discord.ext import commands


class Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup",
        description="Setup Deepwoken carry system"
    )
    async def setup(
        self,
        interaction: discord.Interaction
    ):

        guild = interaction.guild


        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You need Administrator permission.",
                ephemeral=True
            )
            return


        await interaction.response.defer(
            ephemeral=True
        )


        # CATEGORY

        category = discord.utils.get(
            guild.categories,
            name="Deepwoken Carry"
        )


        if category is None:

            category = await guild.create_category(
                "Deepwoken Carry"
            )


        # CHANNELS

        channel_names = [
            "carry-hosts",
            "incident-reports",
            "logs"
        ]


        channels = {}


        for name in channel_names:

            channel = discord.utils.get(
                guild.text_channels,
                name=name
            )


            if channel is None:

                channel = await guild.create_text_channel(
                    name=name,
                    category=category
                )


            channels[name] = channel.id



        # ROLES

        role_names = [

            "Titus Hoster",
            "Elder Primadon Hoster",
            "Heart of Enmity Hoster",

            "Titus Ping",
            "Elder Primadon Ping",
            "Heart of Enmity Ping"

        ]


        roles = {}


        for name in role_names:

            role = discord.utils.get(
                guild.roles,
                name=name
            )


            if role is None:

                role = await guild.create_role(
                    name=name,
                    mentionable=True,
                    reason="Deepwoken carry system"
                )


            roles[name] = role.id



        # SAVE SETTINGS

        if not hasattr(self.bot, "settings"):

            self.bot.settings = {}


        self.bot.settings[guild.id] = {

            "category": category.id,

            "channels": channels,

            "roles": roles

        }



        await interaction.followup.send(
            "Setup completed.\n\n"
            "Created channels:\n"
            "- carry-hosts\n"
            "- incident-reports\n"
            "- logs\n\n"
            "Created roles:\n"
            "- Titus Hoster\n"
            "- Elder Primadon Hoster\n"
            "- Heart of Enmity Hoster\n"
            "- Titus Ping\n"
            "- Elder Primadon Ping\n"
            "- Heart of Enmity Ping"
        )



async def setup(bot):

    await bot.add_cog(
        Setup(bot)
    )
