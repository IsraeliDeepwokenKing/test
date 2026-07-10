import discord
import random
import string

from discord import app_commands
from discord.ext import commands

from views.carry_buttons import CarryButtons
from utils.permissions import create_carry_role


BOSSES = {

    "Titus": {
        "hoster": "Titus Hoster",
        "ping": "Titus Ping",
        "max": 6,
        "min": 1
    },

    "Elder": {
        "hoster": "Elder Hoster",
        "ping": "Elder Ping",
        "max": 10,
        "min": 1
    },

    "Enmity": {
        "hoster": "Enmity Hoster",
        "ping": "Enmity Ping",
        "max": 10,
        "min": 5
    }

}


def generate_id():

    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )


class Host(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(
        name="host",
        description="Create a Deepwoken boss carry"
    )
    @app_commands.describe(
        boss="Choose boss",
        players="Maximum players for this carry"
    )
    @app_commands.choices(

        boss=[

            app_commands.Choice(
                name="Titus",
                value="Titus"
            ),

            app_commands.Choice(
                name="Elder",
                value="Elder"
            ),

            app_commands.Choice(
                name="Enmity",
                value="Enmity"
            )

        ]

    )

    async def host(
        self,
        interaction: discord.Interaction,
        boss: app_commands.Choice[str],
        players: int
    ):


        guild = interaction.guild
        user = interaction.user


        data = BOSSES[boss.value]



        # Check host role

        role = discord.utils.get(
            guild.roles,
            name=data["hoster"]
        )


        if role not in user.roles:

            await interaction.response.send_message(
                f"You need {data['hoster']} role.",
                ephemeral=True
            )

            return



        # Player limit

        if players < data["min"]:

            await interaction.response.send_message(
                f"{boss.value} requires at least {data['min']} players.",
                ephemeral=True
            )

            return



        if players > data["max"]:

            await interaction.response.send_message(
                f"{boss.value} maximum is {data['max']} players.",
                ephemeral=True
            )

            return



        await interaction.response.defer()



        carry_id = generate_id()



        if not hasattr(self.bot, "carries"):

            self.bot.carries = {}



        while carry_id in self.bot.carries:

            carry_id = generate_id()



        # Stage

        stage_name = (
            f"{boss.value.lower()}-"
            f"{user.name.lower()}-"
            f"{carry_id}"
        )


        stage = await guild.create_stage_channel(
            name=stage_name
        )



        # Carry role

        carry_role = await create_carry_role(
            guild,
            carry_id
        )



        self.bot.carries[carry_id] = {


            "id": carry_id,

            "guild": guild.id,

            "boss": boss.value,

            "host": user.id,


            "role": carry_role.id,

            "stage": stage.id,


            "max": players,

            "min": data["min"],



            "active": [],

            "waiting": [],



            "join_log": [],

            "leave_log": [],



            "message": None,

            "channel": None

        }



        ping_role = discord.utils.get(
            guild.roles,
            name=data["ping"]
        )


        ping = ""

        if ping_role:

            ping = ping_role.mention



        embed = discord.Embed(

            title=f"{boss.value} Carry",

            description=f"""

Carry ID:
`{carry_id}`


Host:
{user.mention}


Players:
0/{players}


Active

① -
② -
③ -
④ -
⑤ -
⑥ -
⑦ -
⑧ -
⑨ -
⑩ -


Waiting

None


Stage:
{stage.mention}


Status:
Open

"""

        )



        channel = discord.utils.get(
            guild.text_channels,
            name="carry-hosts"
        )


        if channel is None:

            await interaction.followup.send(
                "Missing carry-hosts channel. Run /setup.",
                ephemeral=True
            )

            return



        message = await channel.send(

            content=ping,

            embed=embed,

            view=CarryButtons(
                self.bot,
                carry_id
            )

        )



        self.bot.carries[carry_id]["message"] = message.id

        self.bot.carries[carry_id]["channel"] = channel.id



        await interaction.followup.send(

            f"Carry created.\nID: `{carry_id}`",

            ephemeral=True

        )



async def setup(bot):

    await bot.add_cog(
        Host(bot)
    )
