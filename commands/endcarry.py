import discord

from discord.ext import commands
from discord import app_commands

from managers.carry_manager import carry_manager
from managers.log_manager import log_manager
from utils.permissions import permission_manager


class EndCarry(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="endcarry",
        description="Ends one of your carries."
    )

    @app_commands.describe(
        carry_id="Carry ID"
    )

    async def endcarry(

        self,

        interaction: discord.Interaction,

        carry_id: str

    ):

        await interaction.response.defer(
            ephemeral=True
        )

        carry_id = carry_id.upper()

        carry = carry_manager.get(
            carry_id
        )

        if carry is None:

            await interaction.followup.send(

                "Carry not found.",

                ephemeral=True

            )

            return

        if interaction.user.id != carry["host_id"]:

            await interaction.followup.send(

                "Only the host can end this carry.",

                ephemeral=True

            )

            return

        guild = interaction.guild

        role = guild.get_role(
            carry["role_id"]
        )

        channel = guild.get_channel(
            carry["channel_id"]
        )

        stage = guild.get_channel(
            carry["stage_id"]
        )
                # ----------------------------
        # REMOVE ROLES
        # ----------------------------

        if role:

            for uid in carry["active"]:

                member = guild.get_member(uid)

                if member:

                    try:

                        await permission_manager.remove_carry_role(
                            member,
                            role
                        )

                    except Exception as e:

                        print(
                            f"Failed removing role from {uid}:",
                            e
                        )

        # ----------------------------
        # DELETE MESSAGE
        # ----------------------------

        if channel:

            try:

                message = await channel.fetch_message(
                    carry["message_id"]
                )

                await message.delete()

            except Exception as e:

                print(
                    "Message delete failed:",
                    e
                )

        # ----------------------------
        # DELETE STAGE
        # ----------------------------

        if stage:

            try:

                await stage.delete(
                    reason="Carry Ended"
                )

            except Exception as e:

                print(
                    "Stage delete failed:",
                    e
                )

        # ----------------------------
        # DELETE TEMP ROLE
        # ----------------------------

        if role:

            try:

                await role.delete(
                    reason="Carry Ended"
                )

            except Exception as e:

                print(
                    "Role delete failed:",
                    e
                )

        # ----------------------------
        # CLEAR LOGS
        # ----------------------------

        try:

            log_manager.clear(
                carry_id
            )

        except Exception as e:

            print(
                "Log delete failed:",
                e
            )

        # ----------------------------
        # DELETE DATABASE ENTRY
        # ----------------------------

        carry_manager.delete(
            carry_id
        )

        # ----------------------------
        # FINISHED
        # ----------------------------

        await interaction.followup.send(

            f"✅ Carry **{carry_id}** ended successfully.",

            ephemeral=True

        )


async def setup(bot):

    await bot.add_cog(
        EndCarry(bot)
    )
