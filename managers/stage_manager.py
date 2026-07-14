import discord


class StageManager:

    async def create(
        self,
        guild: discord.Guild,
        carry_id: str,
        boss: str,
        host: discord.Member,
        carry_role: discord.Role
    ):

        overwrites = {

            guild.default_role: discord.PermissionOverwrite(
                view_channel=False,
                connect=False
            ),

            carry_role: discord.PermissionOverwrite(
                view_channel=True,
                connect=True,
                speak=False
            ),

            host: discord.PermissionOverwrite(
                view_channel=True,
                connect=True,
                speak=True,
                mute_members=True,
                move_members=True
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

        stage = guild.get_channel(stage_id)

        if stage is None:

            try:

                stage = await guild.fetch_channel(
                    stage_id
                )

            except discord.NotFound:

                return

        await stage.delete(
            reason="Carry Ended"
        )


    async def sync_permissions(
        self,
        guild: discord.Guild,
        carry_id: str
    ):
        # Više nije potreban.
        # Pristup Stageu kontrolira temporary carry role.
        return


stage_manager = StageManager()
