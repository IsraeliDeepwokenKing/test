import discord
from discord import app_commands
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup",
        description="Setup Deepwoken carry sistema"
    )
    async def setup(self, interaction: discord.Interaction):

        guild = interaction.guild

        await interaction.response.defer(ephemeral=True)


        # Provjera admina
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(
                "Nemaš dozvolu za ovu komandu."
            )
            return


        # Napravi kategoriju
        category = discord.utils.get(
            guild.categories,
            name="Deepwoken Carry"
        )

        if category is None:
            category = await guild.create_category(
                "Deepwoken Carry"
            )


        # Napravi kanale

        channels = {}

        for name in [
            "carry-hosts",
            "incident-reports",
            "logs"
        ]:

            channel = discord.utils.get(
                guild.text_channels,
                name=name
            )

            if channel is None:
                channel = await guild.create_text_channel(
                    name,
                    category=category
                )

            channels[name] = channel.id



        # Roleovi

        roles = {}

        role_names = [
            "Titus Hoster",
            "Elder Primadon Hoster",
            "Heart of Enmity Hoster"
        ]


        for name in role_names:

            role = discord.utils.get(
                guild.roles,
                name=name
            )

            if role is None:
                role = await guild.create_role(
                    name=name,
                    reason="Deepwoken carry setup"
                )

            roles[name] = role.id



        # spremanje privremeno u bot memoriju

        if not hasattr(self.bot, "settings"):
            self.bot.settings = {}

        self.bot.settings[guild.id] = {
            "category": category.id,
            "channels": channels,
            "roles": roles
        }


        await interaction.followup.send(
            "Setup završen.\n\n"
            "Kreirano:\n"
            "- carry-hosts\n"
            "- incident-reports\n"
            "- logs\n\n"
            "Boss roleovi:\n"
            "- Titus Hoster\n"
            "- Elder Primadon Hoster\n"
            "- Heart of Enmity Hoster"
        )



async def setup(bot):
    await bot.add_cog(Setup(bot))
