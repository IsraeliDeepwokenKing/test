import discord

from discord.ext import commands
from discord import app_commands

from managers.carry_manager import carry_manager
from managers.embed_manager import embed_manager
from managers.stage_manager import stage_manager
from utils.permissions import permission_manager

from views.carry_buttons import CarryButtons


BOSS_LIMITS = {

    "Titus": {
        "min": 1,
        "max": 6,
        "ping": "Titus Ping"
    },

    "Elder Primadon": {
        "min": 1,
        "max": 16,
        "ping": "Elder Ping"
    },

    "Heart of Enmity": {
        "min": 5,
        "max": 12,
        "ping": "Enmity Ping"
    }

}


class Host(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="host",
        description="Start a new carry."
    )

    @app_commands.describe(

        boss="Which boss are you hosting?",

        players="Number of players:"

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

        players: app_commands.Range[int, 1, 10]

    ):

        await interaction.response.defer(
            ephemeral=True
        )

        guild = interaction.guild
        host = interaction.user

        boss_name = boss.value

        limits = BOSS_LIMITS[boss_name]
                # -----------------------------
        # BROJ IGRAČA
        # -----------------------------

        if players < limits["min"]:

            await interaction.followup.send(

                f"Minimum amount of players for **{boss_name}** is **{limits['min']}**.",

                ephemeral=True

            )

            return

        if players > limits["max"]:

            await interaction.followup.send(

                f"Maximum amount of players for **{boss_name}** is **{limits['max']}**.",

                ephemeral=True

            )

            return


        # -----------------------------
        # HOST ROLE
        # -----------------------------

        if not permission_manager.has_host_role(
            host,
            boss_name
        ):

            await interaction.followup.send(

                "You dont have the needed role.",

                ephemeral=True

            )

            return


        # -----------------------------
        # VEĆ HOSTA
        # -----------------------------

        if carry_manager.host_has_carry(
            host.id
        ):

            await interaction.followup.send(

                "Carry is already active.",

                ephemeral=True

            )

            return
                # -----------------------------
        # CARRY ID
        # -----------------------------

        carry_id = carry_manager.generate_id()

        # -----------------------------
        # CARRY ROLE
        # -----------------------------

        carry_role = await permission_manager.create_carry_role(

            guild,

            carry_id

        )

        # -----------------------------
        # STAGE
        # -----------------------------

        stage = await stage_manager.create(

            guild,

            carry_id,

            boss_name,

            host

        )

        # -----------------------------
        # CARRY PINGS CHANNEL
        # -----------------------------

        ping_channel = discord.utils.get(

            guild.text_channels,

            name="carry-pings"

        )

        if ping_channel is None:

            await interaction.followup.send(

                "Missing carry channel.",

                ephemeral=True

            )

            await carry_role.delete()

            await stage.delete()

            return

        # -----------------------------
        # SPREMI U BAZU
        # -----------------------------

        carry_manager.create(

            carry_id=carry_id,

            guild_id=guild.id,

            host_id=host.id,

            boss=boss_name,

            max_players=players,

            stage_id=stage.id,

            message_id=0,

            channel_id=ping_channel.id,

            role_id=carry_role.id

        )

                # -----------------------------
        # PING ROLE
        # -----------------------------

        ping_role = permission_manager.get_ping_role(
            guild,
            boss_name
        )

        ping_text = ""

        if ping_role is not None:

            ping_text = ping_role.mention

        # -----------------------------
        # EMBED
        # -----------------------------

        embed = await embed_manager.build(

            guild,

            carry_id

        )

        # -----------------------------
        # BUTTONS
        # -----------------------------

        view = CarryButtons(

            self.bot,

            carry_id

        )

        # -----------------------------
        # SEND MESSAGE
        # -----------------------------

        message = await ping_channel.send(

            content=ping_text,

            embed=embed,

            view=view,

            allowed_mentions=discord.AllowedMentions(
                roles=True
            )

        )

        # -----------------------------
        # SAVE MESSAGE ID
        # -----------------------------

        carry_manager.set_message(

            carry_id,

            message.id

        )

        # -----------------------------
        # UPDATE EMBED
        # -----------------------------

        await embed_manager.update_message(

            guild,

            carry_id

        )

        # -----------------------------
        # UPDATE STAGE
        # -----------------------------

        await stage_manager.sync_permissions(

            guild,

            carry_id

        )
                # -----------------------------
        # GOTOVO
        # -----------------------------

        # Ne šaljemo "Carry created"
        # jer se carry odmah vidi u
        # #carry-pings kanalu.

        return


async def setup(bot):

    await bot.add_cog(

        Host(bot)

    )
