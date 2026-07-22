import discord

from database import execute, fetchone


class GiveawayClaimView(discord.ui.View):

    def __init__(self, giveaway_id: str):

        super().__init__(timeout=None)

        self.giveaway_id = giveaway_id


    @discord.ui.button(
        label="Claim",
        style=discord.ButtonStyle.green,
        emoji="🎁",
        custom_id="giveaway_claim"
    )
    async def claim(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        winner = fetchone(
            """
            SELECT *
            FROM giveaway_winners
            WHERE giveaway_id = ?
            AND user_id = ?
            """,
            (
                self.giveaway_id,
                interaction.user.id
            )
        )

        if winner is None:

            await interaction.response.send_message(
                "You are not a winner.",
                ephemeral=True
            )

            return

        if winner["claimed"]:

            await interaction.response.send_message(
                "You have already claimed this prize.",
                ephemeral=True
            )

            return

        execute(
            """
            UPDATE giveaway_winners
            SET claimed = 1,
                claimed_at = ?
            WHERE giveaway_id = ?
            AND user_id = ?
            """,
            (
                int(discord.utils.utcnow().timestamp()),
                self.giveaway_id,
                interaction.user.id
            )
        )
                giveaway = fetchone(
            """
            SELECT *
            FROM giveaways
            WHERE giveaway_id = ?
            """,
            (
                self.giveaway_id,
            )
        )

        try:

            guild = interaction.client.get_guild(
                giveaway["guild_id"]
            )

            channel = guild.get_channel(
                giveaway["channel_id"]
            )

            message = await channel.fetch_message(
                giveaway["message_id"]
            )

            await message.add_reaction("✅")

            embed = message.embeds[0]

            embed.add_field(
                name="Claimed",
                value=interaction.user.mention,
                inline=False
            )

            await message.edit(
                embed=embed
            )

        except Exception:
            pass

        for item in self.children:

            item.disabled = True

        await interaction.response.edit_message(
            content="Prize claimed successfully.",
            view=self
        )
