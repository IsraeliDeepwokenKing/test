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
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
            host: discord.PermissionOverwrite(
                view_channel=True,
                connect=True,
                speak=True
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

        try:

            stage = guild.get_channel(stage_id)

            if stage is None:
                stage = await guild.fetch_channel(stage_id)

            await stage.delete(
                reason="Carry ended"
            )

        except discord.NotFound:
            pass

        except discord.Forbidden:
            raise

        except Exception:
            raise


    async def sync_permissions(
        self,
        guild: discord.Guild,
        carry_id: str
    ):

        carry = carry_manager.get(carry_id)

        if carry is None:
            return

        stage = guild.get_channel(int(carry["stage_id"]))

        if stage is None:

            try:
                stage = await guild.fetch_channel(
                    int(carry["stage_id"])
                )
            except discord.NotFound:
                return

        host = guild.get_member(
            int(carry["host_id"])
        )

        for target in list(stage.overwrites):

            if isinstance(target, discord.Member):

                if host and target.id == host.id:
                    continue

                await stage.set_permissions(
                    target,
                    overwrite=None
                )

        if host:

            await stage.set_permissions(
                host,
                view_channel=True,
                connect=True,
                speak=True
            )

        for uid in carry["active"]:

            member = guild.get_member(int(uid))

            if member:

                await stage.set_permissions(
                    member,
                    view_channel=True,
                    connect=True,
                    speak=False
                )

        # Waiting igrači nemaju pristup Stageu


stage_manager = StageManager()
