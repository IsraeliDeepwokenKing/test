import discord

from database import execute

from discord.ext import commands
from discord import app_commands

from database import fetchone
from managers.giveaway_manager import GiveawayManager
from views.giveaway_view import GiveawayView
from utils.discord_time import discord_timestamp


class Giveaway(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.manager = GiveawayManager()

    giveaway = app_commands.Group(
        name="giveaway",
        description="Giveaway commands."
    )

    @giveaway.command(
        name="create",
        description="Create a giveaway."
    )

    @app_commands.describe(
        prize="Prize",
        winners="Number of winners",
        duration="Example: 30m, 2h, 1d",
        reroll="Example: 24h",
        required_role="Optional required role"
    )

    async def create(

        self,

        interaction: discord.Interaction,

        prize: str,

        winners: int,

        duration: str,

        reroll: str,

        required_role: discord.Role | None = None

    ):

        config = fetchone(
            """
            SELECT *
            FROM guild_config
            WHERE guild_id = ?
            """,
            (
                interaction.guild.id,
            )
        )

        if config is None:

            await interaction.response.send_message(
                "Server has not been setup.",
                ephemeral=True
            )

            return

        if interaction.channel.id != config["giveaway_channel_id"]:

            await interaction.response.send_message(
                "This command can only be used in the giveaway channel.",
                ephemeral=True
            )

            return

        giveaway_role = interaction.guild.get_role(
            config["giveaway_role_id"]
        )

        if giveaway_role is None:

            await interaction.response.send_message(
                "Giveaway Manager role no longer exists.",
                ephemeral=True
            )

            return

        if giveaway_role not in interaction.user.roles:

            await interaction.response.send_message(
                "You don't have permission to create giveaways.",
                ephemeral=True
            )

            return

        giveaway = self.manager.create(

            guild_id=interaction.guild.id,

            channel_id=interaction.channel.id,

            host_id=interaction.user.id,

            prize=prize,

            winners=winners,

            duration=duration,

            reroll=reroll
        )

        embed = discord.Embed(
        title="🎉 Giveaway",
        color=discord.Color.gold()
        )

        embed.add_field(
            name="Prize",
            value=prize,
            inline=False
        )

        embed.add_field(
            name="Hosted By",
            value=interaction.user.mention,
            inline=True
        )

        embed.add_field(
            name="Winners",
            value=str(winners),
            inline=True
        )

        embed.add_field(
            name="Ends",
            value=discord_timestamp(
                giveaway["ends"],
                "F"
            ),
            inline=False
        )

        embed.add_field(
            name="Time Remaining",
            value=discord_timestamp(
                giveaway["ends"],
                "R"
            ),
            inline=False
        )

        embed.add_field(
            name="Reroll Time",
            value=reroll,
            inline=False
        )

        if required_role is not None:

            embed.add_field(
                name="Required Role",
                value=required_role.mention,
                inline=False
            )

        embed.set_footer(
            text=f"Giveaway ID • {giveaway['id']}"
        )

        message = await interaction.channel.send(
            embed=embed,
            view=GiveawayView(
                self.manager,
                giveaway["id"]
            )
        )

        self.manager.db.execute(
            """
            UPDATE giveaways
            SET message_id = ?,
                role_requirement = ?
            WHERE giveaway_id = ?
            """,
            (
                message.id,
                required_role.id if required_role else None,
                giveaway["id"]
            )
        )

        await interaction.response.send_message(
            "✅ Giveaway created successfully.",
            ephemeral=True
        )
async def setup(bot):
    await bot.add_cog(Giveaway(bot))
