import discord
from discord.ext import commands
from discord import app_commands


class CloseIncidentModal(discord.ui.Modal, title="Close Incident"):

    punishment = discord.ui.TextInput(
        label="Punishment",
        placeholder="Warn / Kick / Ban / Blacklist / None",
        required=True,
        max_length=100
    )

    notes = discord.ui.TextInput(
        label="Notes",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):

        logs = discord.utils.get(
            interaction.guild.text_channels,
            name="incident-logs"
        )

        if logs:

            embed = discord.Embed(
                title="✅ Incident Closed",
                colour=discord.Colour.green()
            )

            embed.add_field(
                name="Ticket",
                value=interaction.channel.name,
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=interaction.user.mention,
                inline=False
            )

            embed.add_field(
                name="Punishment",
                value=self.punishment.value,
                inline=False
            )

            embed.add_field(
                name="Notes",
                value=self.notes.value or "None",
                inline=False
            )

            await logs.send(embed=embed)

        await interaction.response.send_message(
            "Incident closed.\nDeleting ticket...",
            ephemeral=True
        )

        await interaction.channel.delete(
            reason=f"Closed by {interaction.user}"
        )


class IncidentClose(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="closeincident",
        description="Close an incident ticket."
    )
    async def closeincident(
        self,
        interaction: discord.Interaction
    ):

        if not interaction.channel.name.startswith("incident-"):
            return await interaction.response.send_message(
                "This command can only be used inside an incident ticket.",
                ephemeral=True
            )

        await interaction.response.send_modal(
            CloseIncidentModal()
        )


async def setup(bot):
    await bot.add_cog(
        IncidentClose(bot)
    )
