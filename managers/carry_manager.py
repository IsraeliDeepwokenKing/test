import discord

from discord.ui import View, Button

from managers.carry_manager import carry_manager
from managers.queue_manager import queue_manager
from managers.embed_manager import embed_manager
from managers.stage_manager import stage_manager
from managers.log_manager import log_manager
from managers.blacklist_manager import blacklist_manager

from utils.permissions import permission_manager


class JoinButton(Button):

    def __init__(self, carry_id: str):

        super().__init__(

            label="Join",

            style=discord.ButtonStyle.green,

            custom_id=f"join:{carry_id}"

        )

        self.carry_id = carry_id


    async def callback(
        self,
        interaction: discord.Interaction
    ):

        carry = carry_manager.get(
            self.carry_id
        )

        if carry is None:

            await interaction.response.send_message(

                "Carry više ne postoji.",

                ephemeral=True

            )

            return

        # ------------------------
        # HOST NE MOŽE JOINATI
        # ------------------------

        if interaction.user.id == carry["host_id"]:

            await interaction.response.send_message(

                "Ne možeš se pridružiti vlastitom carryju.",

                ephemeral=True

            )

            return

        # ------------------------
        # BLACKLIST
        # ------------------------

        if blacklist_manager.is_blacklisted(

            carry["host_id"],

            interaction.user.id

        ):

            await interaction.response.send_message(

                "Host te je blacklistao.",

                ephemeral=True

            )

            return

        # ------------------------
        # JOIN
        # ------------------------

        success, location = queue_manager.join(

            self.carry_id,

            interaction.user.id

        )

        if not success:

            await interaction.response.send_message(

                location,

                ephemeral=True

            )

            return
                # ------------------------
        # LOG
        # ------------------------

        if location == "active":

            log_manager.add(

                self.carry_id,

                interaction.user.id,

                "join_active"

            )

        else:

            log_manager.add(

                self.carry_id,

                interaction.user.id,

                "join_waiting"

            )


        # ------------------------
        # GIVE CARRY ROLE
        # ------------------------

        carry = carry_manager.get(
            self.carry_id
        )

        role = interaction.guild.get_role(
            carry["role_id"]
        )

        if role:

            await permission_manager.give_carry_role(

                interaction.user,

                role

            )


        # ------------------------
        # UPDATE STAGE
        # ------------------------

        await stage_manager.sync_permissions(

            interaction.guild,

            self.carry_id

        )


        # ------------------------
        # UPDATE EMBED
        # ------------------------

        await embed_manager.update_message(

            interaction.guild,

            self.carry_id

        )


        # ------------------------
        # RESPONSE
        # ------------------------

        if location == "active":

            msg = "Dodan si u Active listu."

        else:

            msg = "Active je pun. Dodan si u Waiting listu."


        await interaction.response.send_message(

            msg,

            ephemeral=True

        )
        class LeaveButton(Button):

    def __init__(self, carry_id: str):

        super().__init__(

            label="Leave",

            style=discord.ButtonStyle.red,

            custom_id=f"leave:{carry_id}"

        )

        self.carry_id = carry_id


    async def callback(
        self,
        interaction: discord.Interaction
    ):

        carry = carry_manager.get(
            self.carry_id
        )

        if carry is None:

            await interaction.response.send_message(

                "Carry više ne postoji.",

                ephemeral=True

            )

            return


        # ------------------------
        # LEAVE
        # ------------------------

        success, promoted = queue_manager.leave(

            self.carry_id,

            interaction.user.id

        )

        if not success:

            await interaction.response.send_message(

                promoted,

                ephemeral=True

            )

            return


        # ------------------------
        # REMOVE ROLE
        # ------------------------

        role = interaction.guild.get_role(
            carry["role_id"]
        )

        if role:

            await permission_manager.remove_carry_role(

                interaction.user,

                role

            )


        # ------------------------
        # LOG LEAVE
        # ------------------------

        log_manager.add(

            self.carry_id,

            interaction.user.id,

            "leave"

        )


        # ------------------------
        # PROMOTION
        # ------------------------

        if promoted is not None:

            promoted_member = interaction.guild.get_member(
                promoted
            )

            if promoted_member:

                if role:

                    await permission_manager.give_carry_role(

                        promoted_member,

                        role

                    )

                log_manager.add(

                    self.carry_id,

                    promoted,

                    "promoted"

                )


        # ------------------------
        # UPDATE STAGE
        # ------------------------

        await stage_manager.sync_permissions(

            interaction.guild,

            self.carry_id

        )


        # ------------------------
        # UPDATE EMBED
        # ------------------------

        await embed_manager.update_message(

            interaction.guild,

            self.carry_id

        )


        # ------------------------
        # RESPONSE
        # ------------------------

        await interaction.response.send_message(

            "Napustio si carry.",

            ephemeral=True

        )
        class CarryButtons(View):

    def __init__(self, bot, carry_id: str):

        super().__init__(timeout=None)

        self.bot = bot
        self.carry_id = carry_id

        self.add_item(
            JoinButton(carry_id)
        )

        self.add_item(
            LeaveButton(carry_id)
        )
