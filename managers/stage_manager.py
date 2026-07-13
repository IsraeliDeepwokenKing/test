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

            name="temp-stage",

            overwrites=overwrites,

            reason="Deepwoken Carry"

        )

        return stage



    async def delete(
        self,
        guild: discord.Guild,
        stage_id: int
    ):

        stage = guild.get_channel(stage_id)

        if stage:

            await stage.delete()



    async def sync_permissions(
        for overwrite in list(stage.overwrites):

    target = overwrite

    if isinstance(target, discord.Member):

        if host and target.id == host.id:
            continue

        await stage.set_permissions(
            target,
            overwrite=None
        )
        self,
        guild: discord.Guild,
        carry_id: str
    ):

        carry = carry_manager.get(carry_id)

        if carry is None:
            return

        stage = guild.get_channel(
            carry["stage_id"]
        )

        if stage is None:
            return

        host = guild.get_member(
            carry["host_id"]
        )

        if host:

            await stage.set_permissions(

                host,

                view_channel=True,
                connect=True,
                speak=True

            )

        active = carry["active"]

        waiting = carry["waiting"]

        for uid in active:

            member = guild.get_member(uid)

            if member:

                await stage.set_permissions(

                    member,

                    view_channel=True,
                    connect=True,
                    speak=False

                )

        for uid in waiting:

            member = guild.get_member(uid)

            if member:

                await stage.set_permissions(

                    member,

                    overwrite=None

                )



stage_manager = StageManager()
