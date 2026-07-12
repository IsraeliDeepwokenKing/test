import discord
from discord import app_commands
from discord.ext import commands

from managers.host_manager import host_manager
from managers.carry_manager import carry_manager
from managers.log_manager import log_manager
from utils.permissions import permission_manager

from views.carry_buttons import CarryButtons


BOSSES = {

    "Titus": {
        "minimum": 1,
        "maximum": 6
    },

    "Elder": {
        "minimum": 1,
        "maximum": 1
    },

    "Enmity": {
        "minimum": 5,
        "maximum": 10
    }

}


class Host(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="host",
        description="Start new carry."
    )

    @app_commands.describe(

        boss="Which boss?",

        players="How many players?"

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

        member = interaction.user

        boss_name = boss.value
                # -----------------------------
        # VALIDACIJA BROJA IGRAČA
        # -----------------------------

        boss_data = BOSSES[boss_name]

        if players < boss_data["minimum"]:

            await interaction.followup.send(

                f"Min amount of players for **{boss_name}** is **{boss_data['minimum']}**.",

                ephemeral=True

            )

            return


        if players > boss_data["maximum"]:

            await interaction.followup.send(

                f"Max amount of players for **{boss_name}** is **{boss_data['maximum']}**.",

                ephemeral=True

            )

            return


        # -----------------------------
        # HOST ROLE
        # -----------------------------

        if not permission_manager.has_host_role(
            member,
            boss_name
        ):

            await interaction.followup.send(

                "You dont have the needed role.",

                ephemeral=True

            )

            return


        # -----------------------------
        # VEĆ POSTOJI CARRY
        # -----------------------------

        if carry_manager.host_has_carry(
            member.id
        ):

            await interaction.followup.send(

                "You are already hosting a carry.",

                ephemeral=True

            )

            return


        # -----------------------------
        # CARRY PINGS CHANNEL
        # -----------------------------

        ping_channel = discord.utils.get(

            guild.text_channels,

            name="carry-pings"

        )

        if ping_channel is None:

            await interaction.followup.send(

                "Missing ping channel, use /setup command.",

                ephemeral=True

            )

            return


        # -----------------------------
        # CREATE HOST
        # -----------------------------

        try:

            carry_id, carry_role, stage = await host_manager.create_host(

                guild,

                member,

                boss_name,

                players,

                ping_channel

            )

        except Exception as e:

            await interaction.followup.send(

                str(e),

                ephemeral=True

            )

            return
                # -----------------------------
        # PING ROLE
        # -----------------------------

        ping_role = permission_manager.get_ping_role(
            guild,
            boss_name
        )

        ping = ""

        if ping_role:

            ping = ping_role.mention


        # -----------------------------
        # ACTIVE LIST
        # -----------------------------

        active = ""

        for i in range(players):

            active += f"{i + 1}. —\n"


        # -----------------------------
        # EMBED
        # -----------------------------

        embed = discord.Embed(

            title=f"{boss_name} Carry",

            colour=discord.Colour.blurple()

        )

        embed.add_field(

            name="Carry ID",

            value=f"`{carry_id}`",

            inline=False

        )

        embed.add_field(

            name="Host",

            value=member.mention,

            inline=False

        )

        embed.add_field(

            name=f"Active (0/{players})",

            value=active,

            inline=False

        )

        embed.add_field(

            name="Waiting (0)",

            value="None",

            inline=False

        )

        embed.set_footer(

            text="Deepwoken CarryBot"

        )


        # -----------------------------
        # SEND MESSAGE
        # -----------------------------

        message = await ping_channel.send(

            content=ping,

            embed=embed,

            view=CarryButtons(
                self.bot,
                carry_id
            ),

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
        # LOG HOST
        # -----------------------------

        log_manager.add(

            carry_id,

            member.id,

            "host_created"

        )


        # -----------------------------
        # UPDATE STAGE PERMISSIONS
        # -----------------------------

        from managers.stage_manager import stage_manager

        await stage_manager.sync_permissions(

            guild,

            carry_id

        )


        # -----------------------------
        # NO SUCCESS MESSAGE
        # -----------------------------

        # Namjerno ne šaljemo
        # "Carry created"

        # Hoster će vidjeti carry
        # u carry-pings kanalu.

        return
    async def setup(bot):
    await bot.add_cog(
        Host(bot)
    )
