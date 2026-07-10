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
        custom_id="carry_join"
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
                "This carry no longer exists.",
                ephemeral=True
            )

            return



        user = interaction.user
        user_id = user.id



        if user_id in carry["active"] or user_id in carry["waiting"]:

            await interaction.response.send_message(
                "You are already in this queue.",
                ephemeral=True
            )

            return



        guild = interaction.guild


        role = guild.get_role(
            carry["role"]
        )



        if len(carry["active"]) < carry["max"]:


            carry["active"].append(
                user_id
            )


            await give_carry_role(
                user,
                role
            )


            location = "Active"



        else:


            carry["waiting"].append(
                user_id
            )


            location = "Waiting"




        # JOIN LOG

        carry["join_log"].append({

            "user": user_id,

            "time": discord.utils.utcnow(),

            "location": location

        })



        await update_carry_message(
            self.bot,
            carry
        )



        await interaction.response.send_message(

            f"You joined as {location}.",

            ephemeral=True

        )





    @discord.ui.button(
        label="Leave",
        style=discord.ButtonStyle.red,
        custom_id="carry_leave"
    )
    async def leave(

        self,
        interaction: discord.Interaction,
        button: discord.ui.Button

    ):


        carry = self.bot.carries.get(
            self.carry_id
        )


        if not carry:

            await interaction.response.send_message(
                "This carry no longer exists.",
                ephemeral=True
            )

            return



        user = interaction.user
        user_id = user.id

        guild = interaction.guild


        role = guild.get_role(
            carry["role"]
        )



        promoted = None



        if user_id in carry["active"]:


            carry["active"].remove(
                user_id
            )


            await remove_carry_role(
                user,
                role
            )



            # Move waiting player

            if len(carry["waiting"]) > 0:


                promoted = carry["waiting"].pop(0)


                carry["active"].append(
                    promoted
                )


                new_member = guild.get_member(
                    promoted
                )


                if new_member:

                    await give_carry_role(
                        new_member,
                        role
                    )



        elif user_id in carry["waiting"]:


            carry["waiting"].remove(
                user_id
            )



        else:


            await interaction.response.send_message(

                "You are not in this queue.",

                ephemeral=True

            )

            return




        # LEAVE LOG

        carry["leave_log"].append({

            "user": user_id,

            "time": discord.utils.utcnow()

        })



        await update_carry_message(
            self.bot,
            carry
        )



        message = "You left the carry."


        if promoted:

            member = guild.get_member(
                promoted
            )

            if member:

                message += (
                    f"\n{member.mention} moved "
                    "from waiting to active."
                )



        await interaction.response.send_message(

            message,

            ephemeral=True

        )





async def update_carry_message(bot, carry):


    guild = bot.get_guild(
        carry["guild"]
    )


    channel = guild.get_channel(
        carry["channel"]
    )


    message = await channel.fetch_message(
        carry["message"]
    )



    active_text = ""


    for i in range(carry["max"]):


        if i < len(carry["active"]):

            member = guild.get_member(
                carry["active"][i]
            )

            if member:

                active_text += (
                    f"①②③④⑤⑥⑦⑧⑨⑩"[i]
                    + f" {member.mention}\n"
                )

        else:

            active_text += (
                f"{i+1}. -\n"
            )




    waiting_text = ""


    if carry["waiting"]:


        for i, uid in enumerate(carry["waiting"]):

            member = guild.get_member(
                uid
            )

            waiting_text += (
                f"{i+1}. "
                f"{member.mention}\n"
            )

    else:

        waiting_text = "None"



    embed = discord.Embed(

        title=f"{carry['boss']} Carry",

        description=f"""

Carry ID:
`{carry['id']}`


Host:
<@{carry['host']}>


Active ({len(carry['active'])}/{carry['max']})

{active_text}


Waiting ({len(carry['waiting'])})

{waiting_text}


Status:
Open

"""

    )


    await message.edit(
        embed=embed
    )
