import discord
import random
import string

from discord import app_commands
from discord.ext import commands

from views.carry_buttons import CarryButtons
from utils.permissions import create_carry_role


BOSSES = {
    "Titus": {
        "role": "Titus Hoster",
        "max": 6,
        "min": 1
    },

    "Elder Primadon": {
        "role": "Elder Primadon Hoster",
        "max": 10,
        "min": 1
    },

    "Heart of Enmity": {
        "role": "Heart of Enmity Hoster",
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

        selected = BOSSES[boss.value]


        required_role = discord.utils.get(
            guild.roles,
            name=selected["role"]
        )


        if required_role not in user.roles:

            await interaction.response.send_message(
                f"Missing role: {selected['role']}",
                ephemeral=True
            )
            return


        await interaction.response.defer(
            ephemeral=True
        )


        carry_id = generate_id()


        while hasattr(self.bot, "carries") and carry_id in self.bot.carries:
            carry_id = generate_id()



        stage = await guild.create_stage_channel(
            name=f"carry-{carry_id}"
        )


        carry_role = await create_carry_role(
            guild,
            carry_id
        )


        if not hasattr(self.bot, "carries"):
            self.bot.carries = {}


        self.bot.carries[carry_id] = {

            "id": carry_id,

            "guild": guild.id,

            "boss": boss.value,

            "host": user.id,

            "role": carry_role.id,

            "stage": stage.id,

            "max": selected["max"],

            "min": selected["min"],

            "active": [],

            "waiting": [],

            "joined": [],

            "left": [],

            "message": None,

            "channel": None
        }


        embed = discord.Embed(
            title=f"{boss.value} Carry",
            description=f"""
Carry ID:
`{carry_id}`

Host:
{user.mention}


Active (0/{selected["max"]})

1. -
2. -
3. -
4. -
5. -
6. -


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
                "Missing #carry-hosts channel. Run /setup first.",
                ephemeral=True
            )

            return



        message = await channel.send(
            embed=embed,
            view=CarryButtons(
                self.bot,
                carry_id
            )
        )


        self.bot.carries[carry_id]["message"] = message.id
        self.bot.carries[carry_id]["channel"] = channel.id



        await interaction.followup.send(
            f"Carry created: `{carry_id}`",
            ephemeral=True
        )



async def setup(bot):

    await bot.add_cog(
        Host(bot)
    )
