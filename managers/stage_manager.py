import discord


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
                view_channel=False,
                connect=False
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
                reason="Carry Ended"
            )

        except discord.NotFound:
            return

        except discord.Forbidden:
            raise

        except Exception:
            raise


    async def sync_permissions(
        self,
        guild: discord.Guild,
        carry_id: str
    ):
        # Za prvu verziju bota nije potreban.
        # Temporary carry role kontrolira pristup.
        return


stage_manager = StageManager()
