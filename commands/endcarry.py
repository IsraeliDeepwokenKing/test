import discord

from discord import app_commands
from discord.ext import commands

from utils.permissions import remove_carry_role



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
            carry_id
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



        if carry["message"]:


            channel = guild.get_channel(
                carry["channel"]
            )

            if channel:

                try:

                    msg = await channel.fetch_message(
                        carry["message"]
                    )

                    await msg.delete()

                except:

                    pass




        stage = guild.get_channel(
            carry["stage"]
        )

        if stage:

            await stage.delete()



        if role:

            await role.delete()



        del self.bot.carries[carry_id]



        await interaction.followup.send(
            f"Carry `{carry_id}` ended.",
            ephemeral=True
        )



async def setup(bot):

    await bot.add_cog(
        EndCarry(bot)
    )
