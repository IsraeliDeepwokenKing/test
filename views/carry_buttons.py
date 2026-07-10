import discord

from utils.permissions import (
    give_carry_role,
    remove_carry_role
)



class CarryButtons(discord.ui.View):

    def __init__(self, bot, carry_id):

        super().__init__(
            timeout=None
        )

        self.bot = bot
        self.carry_id = carry_id



    @discord.ui.button(
        label="Join",
        style=discord.ButtonStyle.green,
        custom_id="join_carry"
    )
    async def join(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        carry = self.bot.carries.get(
            self.carry_id
        )


        if not carry:

            await interaction.response.send_message(
                "Carry expired.",
                ephemeral=True
            )
            return



        user_id = interaction.user.id



        if user_id in carry["active"] or user_id in carry["waiting"]:

            await interaction.response.send_message(
                "Already in queue.",
                ephemeral=True
            )
            return



        guild = interaction.guild

        member = guild.get_member(
            user_id
        )

        role = guild.get_role(
            carry["role"]
        )


        if len(carry["active"]) < carry["max"]:

            carry["active"].append(
                user_id
            )

            await give_carry_role(
                member,
                role
            )

            place = "Active"


        else:

            carry["waiting"].append(
                user_id
            )

            place = "Waiting"



        carry["joined"].append(
            user_id
        )



        await interaction.response.send_message(
            f"You joined: {place}",
            ephemeral=True
        )



    @discord.ui.button(
        label="Leave",
        style=discord.ButtonStyle.red,
        custom_id="leave_carry"
    )
    async def leave(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        carry = self.bot.carries.get(
            self.carry_id
        )

        user_id = interaction.user.id

        guild = interaction.guild

        role = guild.get_role(
            carry["role"]
        )

        member = guild.get_member(
            user_id
        )



        if user_id in carry["active"]:


            carry["active"].remove(
                user_id
            )


            await remove_carry_role(
                member,
                role
            )


            if carry["waiting"]:

                next_user = carry["waiting"].pop(0)

                carry["active"].append(
                    next_user
                )


                next_member = guild.get_member(
                    next_user
                )


                await give_carry_role(
                    next_member,
                    role
                )



        elif user_id in carry["waiting"]:


            carry["waiting"].remove(
                user_id
            )


        else:

            await interaction.response.send_message(
                "You are not in queue.",
                ephemeral=True
            )
            return



        carry["left"].append(
            user_id
        )


        await interaction.response.send_message(
            "You left the carry.",
            ephemeral=True
        )



async def setup(bot):
    pass
