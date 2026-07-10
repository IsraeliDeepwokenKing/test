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

    "Elder Primadon": {
        "hoster": "Elder Primadon Hoster",
        "ping": "Elder Primadon Ping",
        "max": 10,
        "min": 1
    },

    "Heart of Enmity": {
        "hoster": "Heart of Enmity Hoster",
        "ping": "Heart of Enmity Ping",
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
        boss="Choose boss"
    )
    @app_commands.choices(

        boss=[

            app_commands.Choice(
                name="Titus",
                value="Titus"
            ),

            app_commands.Choice(
                name="Elder Primadon",
                value="Elder Primadon"
            ),

            app_commands.Choice(
                name="Heart of Enmity",
                value="Heart of Enmity"
            )

        ]
    )


    async def host(
        self,
        interaction: discord.Interaction,
        boss: app_commands.Choice[str]
    ):


        guild = interaction.guild
        user = interaction.user


        data = BOSSES[boss.value]


        # Check host role

        host_role = discord.utils.get(
            guild.roles,
            name=data["hoster"]
        )


        if host_role not in user.roles:

            await interaction.response.send_message(
                f"You need {data['hoster']} role.",
                ephemeral=True
            )

            return



        await interaction.response.defer()



        carry_id = generate_id()


        if not hasattr(self.bot, "carries"):

            self.bot.carries = {}



        while carry_id in self.bot.carries:

            carry_id = generate_id()



        # create stage

        stage = await guild.create_stage_channel(
            name=f"carry-{carry_id}"
        )


        # create temporary carry role

        carry_role = await create_carry_role(
            guild,
            carry_id
        )



        self.bot.carries[carry_id] = {


            "id": carry_id,

            "guild": guild.id,

            "boss": boss.value,

            "host": user.id,


            "stage": stage.id,

            "role": carry_role.id,


            "max": data["max"],

            "min": data["min"],


            "active": [],

            "waiting": [],


            "joined": [],

            "left": [],


            "message": None,

            "channel": None

        }



        # boss ping role

        ping_role = discord.utils.get(
            guild.roles,
            name=data["ping"]
        )


        mention = ""

        if ping_role:

            mention = ping_role.mention



        embed = discord.Embed(

            title=f"{boss.value} Carry",

            description=f"""

Carry ID:
`{carry_id}`


Host:
{user.mention}


Active (0/{data['max']})

① —
② —
③ —
④ —
⑤ —
⑥ —


Waiting (0)


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
                "carry-hosts channel missing. Run /setup.",
                ephemeral=True
            )

            return



        message = await channel.send(

            content=mention,

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
