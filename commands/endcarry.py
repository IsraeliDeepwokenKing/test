import discord

from discord import app_commands
from discord.ext import commands
from utils.permissions import permission_manager



class EndCarry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(
        name="endcarry",
        description="End a carry"
    )
    @app_commands.describe(
        carry_id="Carry ID"
    )
    async def endcarry(
        self,
        interaction: discord.Interaction,
        carry_id: str
    ):


        if not hasattr(self.bot, "carries"):

            await interaction.response.send_message(
                "No active carries.",
                ephemeral=True
            )
            return



        carry = self.bot.carries.get(
            carry_id.upper()
        )


        if not carry:

            await interaction.response.send_message(
                "Carry not found.",
                ephemeral=True
            )

            return



        if interaction.user.id != carry["host"]:

            await interaction.response.send_message(
                "Only the host can end this carry.",
                ephemeral=True
            )

            return



        await interaction.response.defer(
            ephemeral=True
        )



        guild = interaction.guild



        # Remove player roles

        role = guild.get_role(
            carry["role"]
        )


        if role:

            for uid in carry["active"]:

                member = guild.get_member(uid)

                if member:

                    await remove_carry_role(
                        member,
                        role
                    )



        # Delete carry message

        try:

            channel = guild.get_channel(
                carry["channel"]
            )


            if channel:

                message = await channel.fetch_message(
                    carry["message"]
                )

                await message.delete()


        except Exception as e:

            print(
                "Message delete error:",
                e
            )



        # Delete stage

        try:

            stage = guild.get_channel(
                carry["stage"]
            )


            if stage:

                await stage.delete(
                    reason="Carry ended"
                )


        except Exception as e:

            print(
                "Stage delete error:",
                e
            )



        # Delete temporary role

        try:

            if role:

                await role.delete(
                    reason="Carry ended"
                )


        except Exception as e:

            print(
                "Role delete error:",
                e
            )



        # Clear memory

        del self.bot.carries[carry_id.upper()]



        await interaction.followup.send(

            f"Carry `{carry_id.upper()}` has been deleted.",

            ephemeral=True

        )



async def setup(bot):

    await bot.add_cog(
        EndCarry(bot)
    )
