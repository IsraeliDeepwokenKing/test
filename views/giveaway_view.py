import discord

from managers.giveaway_manager import GiveawayManager


class GiveawayView(discord.ui.View):

    def __init__(
        self,
        manager: GiveawayManager,
        giveaway_id: str
    ):
        super().__init__(timeout=None)

        self.manager = manager
        self.giveaway_id = giveaway_id

    @discord.ui.button(
        label="Join",
        emoji="🎉",
        style=discord.ButtonStyle.green,
        custom_id="giveaway_join"
    )
    async def join_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        success, message = self.manager.join(
            self.giveaway_id,
            interaction.user
        )

        await interaction.response.send_message(
            message,
            ephemeral=True
        )

    @discord.ui.button(
        label="Leave",
        emoji="❌",
        style=discord.ButtonStyle.red,
        custom_id="giveaway_leave"
    )
    async def leave_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        success, message = self.manager.leave(
            self.giveaway_id,
            interaction.user.id
        )

        await interaction.response.send_message(
            message,
            ephemeral=True
        )
