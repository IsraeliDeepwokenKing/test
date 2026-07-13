import discord

from managers.carry_manager import carry_manager


class StageManager:

    async def create(
        self,
        guild: discord.Guild,
        carry_id: str,
        boss: str,
        host: discord.Member
    ):

        overwrites = {

            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            host:
                discord.PermissionOverwrite(
                    view_channel=True,
                    connect=True,
                    speak=True,
                    request_to_speak=False
                )
        }


        stage = await guild.create_stage_channel(

            name=f"{boss}-{carry_id}",

            overwrites=overwrites,

            reason="Deepwoken Carry"

        )


        return stage



    async def delete(
        self,
        guild: discord.Guild,
        stage_id: int
    ):

        stage = guild.get_channel(
            stage_id
        )

        if stage:

            await stage.delete()



    async def sync_permissions(
        self,
        guild: discord.Guild,
        carry_id: str
    ):

        carry = carry_manager.get(
            carry_id
        )


        if carry is None:
            return


        stage = guild.get_channel(
            int(carry["stage_id"])
        )


        if stage is None:
            return



        host = guild.get_member(
            int(carry["host_id"])
        )


        # ------------------------
        # RESET SVIH STARIH PERMISSIONA
        # ------------------------

        for target, overwrite in list(stage.overwrites.items()):

            if isinstance(target, discord.Member):

                if host and target.id == host.id:
                    continue


                await stage.set_permissions(
                    target,
                    overwrite=None
                )



        # ------------------------
        # HOST
        # ------------------------

        if host:

            await stage.set_permissions(

                host,

                view_channel=True,
                connect=True,
                speak=True

            )



        # ------------------------
        # ACTIVE PLAYERS
        # ------------------------

        for uid in carry.get("active", []):

            member = guild.get_member(
                int(uid)
            )


            if member:

                await stage.set_permissions(

                    member,

                    view_channel=True,
                    connect=True,
                    speak=False

                )



        # ------------------------
        # WAITING PLAYERS
        # ------------------------

        for uid in carry.get("waiting", []):

            member = guild.get_member(
                int(uid)
            )


            if member:

                await stage.set_permissions(

                    member,

                    overwrite=None

                )



stage_manager = StageManager()
