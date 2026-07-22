import discord

from discord.ext import commands
from discord import app_commands

from database import execute


# ==========================================================
# ROLE NAMES
# ==========================================================

BOT_ROLE = "CarryBot"

HOSTER_ROLE = "Hoster"

GIVEAWAY_MANAGER_ROLE = "Giveaway Manager"

BLACKLIST_CERTIFIED_ROLE = "Blacklist Certified"

MODERATOR_ROLE = "Moderator"

TICKET_STAFF_ROLE = "Ticket Staff"

INCIDENT_STAFF_ROLE = "Incident Staff"

SUSPICION_ROLE = "Suspicion"


# ==========================================================
# CATEGORY NAMES
# ==========================================================

HOST_CATEGORY = "Host System"

TICKET_CATEGORY = "Tickets"

MODERATION_CATEGORY = "Moderation"


# ==========================================================
# CHANNEL NAMES
# ==========================================================

HOST_COMMANDS = "host-commands"

GIVEAWAYS = "giveaways"

LEADERBOARD = "leaderboard"

CREATE_TICKET = "create-ticket"

HOSTER_APPLICATIONS = "hoster-applications"

INCIDENT_LOGS = "incident-logs"

MODERATION_LOGS = "moderation-logs"


class Setup(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="setup",
        description="Sets up CarryBot."
    )

    @app_commands.default_permissions(
        administrator=True
    )

    async def setup(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        guild = interaction.guild

        me = guild.me
        
        # ==========================================================
        # HELPERS
        # ==========================================================

        async def get_role(
            name: str,
            colour: discord.Colour = discord.Colour.default(),
            permissions: discord.Permissions | None = None
        ) -> discord.Role:

            role = discord.utils.get(
                guild.roles,
                name=name
            )

            if role is None:

                role = await guild.create_role(
                    name=name,
                    colour=colour,
                    permissions=permissions or discord.Permissions.none(),
                    reason="CarryBot Setup"
                )

            return role


        async def get_category(
            name: str
        ) -> discord.CategoryChannel:

            category = discord.utils.get(
                guild.categories,
                name=name
            )

            if category is None:

                category = await guild.create_category(
                    name=name,
                    reason="CarryBot Setup"
                )

            return category


        async def get_text_channel(
            *,
            name: str,
            category: discord.CategoryChannel,
            overwrites: dict | None = None
        ) -> discord.TextChannel:

            channel = discord.utils.get(
                guild.text_channels,
                name=name
            )

            if channel is None:

                channel = await guild.create_text_channel(
                    name=name,
                    category=category,
                    overwrites=overwrites,
                    reason="CarryBot Setup"
                )

            return channel
        
        # ==========================================================
        # CREATE ROLES
        # ==========================================================

        bot_role = await get_role(
            BOT_ROLE,
            discord.Colour.dark_grey()
        )

        hoster_role = await get_role(
            HOSTER_ROLE,
            discord.Colour.blue()
        )

        giveaway_role = await get_role(
            GIVEAWAY_MANAGER_ROLE,
            discord.Colour.gold()
        )

        blacklist_role = await get_role(
            BLACKLIST_CERTIFIED_ROLE,
            discord.Colour.red()
        )

        moderator_role = await get_role(
            MODERATOR_ROLE,
            discord.Colour.orange()
        )

        ticket_staff_role = await get_role(
            TICKET_STAFF_ROLE,
            discord.Colour.green()
        )

        incident_staff_role = await get_role(
            INCIDENT_STAFF_ROLE,
            discord.Colour.dark_red()
        )

        suspicion_role = await get_role(
            SUSPICION_ROLE,
            discord.Colour.light_grey()
        )
        
        # ==========================================================
        # GIVE BOT ROLE
        # ==========================================================

        if me is not None:

            if bot_role not in me.roles:

                try:

                    await me.add_roles(
                        bot_role,
                        reason="CarryBot Setup"
                    )

                except discord.Forbidden:
                    pass
                
        # ==========================================================
        # CREATE CATEGORIES
        # ==========================================================

        host_category = await get_category(
            HOST_CATEGORY
        )

        moderation_category = await get_category(
            MODERATION_CATEGORY
        )

        ticket_category = await get_category(
            TICKET_CATEGORY
        )
        
        # ==========================================================
        # PERMISSION OVERWRITES
        # ==========================================================

        everyone = guild.default_role

        host_overwrites = {

            everyone: discord.PermissionOverwrite(
                view_channel=False
            ),

            hoster_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True
            ),

            bot_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                manage_channels=True,
                read_message_history=True
            )
        }


        giveaway_overwrites = {

            everyone: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True
            ),

            giveaway_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                use_application_commands=True
            ),

            bot_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True
            )
        }


        leaderboard_overwrites = {

            everyone: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True
            ),

            bot_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True
            )
        }


        staff_overwrites = {

            everyone: discord.PermissionOverwrite(
                view_channel=False
            ),

            moderator_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),

            ticket_staff_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),

            incident_staff_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),

            bot_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                manage_channels=True,
                read_message_history=True
            )
        }


        ticket_panel_overwrites = {

            everyone: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True
            ),

            bot_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True
            )
        }
        
        # ==========================================================
        # CREATE CHANNELS
        # ==========================================================

        host_commands = await get_text_channel(
            name=HOST_COMMANDS,
            category=host_category,
            overwrites=host_overwrites
        )

        giveaway_channel = await get_text_channel(
            name=GIVEAWAYS,
            category=host_category,
            overwrites=giveaway_overwrites
        )

        leaderboard_channel = await get_text_channel(
            name=LEADERBOARD,
            category=host_category,
            overwrites=leaderboard_overwrites
        )

        moderation_logs = await get_text_channel(
            name=MODERATION_LOGS,
            category=moderation_category,
            overwrites=staff_overwrites
        )

        incident_logs = await get_text_channel(
            name=INCIDENT_LOGS,
            category=moderation_category,
            overwrites=staff_overwrites
        )

        ticket_panel = await get_text_channel(
            name=CREATE_TICKET,
            category=ticket_category,
            overwrites=ticket_panel_overwrites
        )

        hoster_applications = await get_text_channel(
            name=HOSTER_APPLICATIONS,
            category=ticket_category,
            overwrites=staff_overwrites
        )
        
        # ==========================================================
        # SAVE CONFIG
        # ==========================================================

        execute(
            """
            INSERT OR REPLACE INTO guild_config(

                guild_id,

                setup_completed,

                giveaway_channel_id,
                giveaway_role_id,

                moderation_log_channel_id,

                ticket_panel_channel_id,

                incident_log_channel_id,

                leaderboard_channel_id,

                hoster_application_channel_id

            )

            VALUES

            (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                guild.id,

                1,

                giveaway_channel.id,
                giveaway_role.id,

                moderation_logs.id,

                ticket_panel.id,

                incident_logs.id,

                leaderboard_channel.id,

                hoster_applications.id
            )
        )

        # ==========================================================
        # LEADERBOARD PLACEHOLDER
        # ==========================================================

        leaderboard_embed = discord.Embed(
            title="🏆 Carry Leaderboard",
            description=(
                "Leaderboard će se automatski osvježavati svakih 90 minuta."
            ),
            color=discord.Color.gold()
        )

        leaderboard_embed.add_field(
            name="Status",
            value="Nema podataka.",
            inline=False
        )

        try:

            await leaderboard_channel.purge(limit=5)

        except Exception:
            pass

        await leaderboard_channel.send(
            embed=leaderboard_embed
        )

        # ==========================================================
        # TICKET PANEL PLACEHOLDER
        # ==========================================================

        ticket_embed = discord.Embed(
            title="🎫 Support Tickets",
            description=(
                "Odaberi vrstu ticketa pomoću gumba ispod."
            ),
            color=discord.Color.blurple()
        )

        ticket_embed.add_field(
            name="Moderation",
            value="Report, appeal ili moderator pomoć.",
            inline=False
        )

        ticket_embed.add_field(
            name="Member Help",
            value="Pitanja vezana uz server ili carry.",
            inline=False
        )

        ticket_embed.add_field(
            name="Hoster Application",
            value="Pošalji prijavu za hostera.",
            inline=False
        )

        try:

            await ticket_panel.purge(limit=5)

        except Exception:
            pass

        await ticket_panel.send(
            embed=ticket_embed
            # view=TicketPanelView()
            # dodat ćemo kasnije bez mijenjanja setupa
        )

        # ==========================================================
        # FINISH
        # ==========================================================

        embed = discord.Embed(
            title="✅ CarryBot Setup Complete",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Host Commands",
            value=host_commands.mention,
            inline=True
        )

        embed.add_field(
            name="Giveaways",
            value=giveaway_channel.mention,
            inline=True
        )

        embed.add_field(
            name="Leaderboard",
            value=leaderboard_channel.mention,
            inline=True
        )

        embed.add_field(
            name="Ticket Panel",
            value=ticket_panel.mention,
            inline=True
        )

        embed.add_field(
            name="Incident Logs",
            value=incident_logs.mention,
            inline=True
        )

        embed.add_field(
            name="Moderation Logs",
            value=moderation_logs.mention,
            inline=True
        )

        embed.add_field(
            name="Hoster Applications",
            value=hoster_applications.mention,
            inline=True
        )

        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )
async def setup(bot):
    await bot.add_cog(Setup(bot))
