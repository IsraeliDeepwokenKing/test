import discord


class StageManager:

    async def create(
        self,
        guild: discord.Guild,
        carry_id: str,
        boss: str,
        host: discord.Member
    ):

        stage = await guild.create_stage_channel(
            name=f"{boss}-{carry_id}",
            reason="Deepwoken Carry"
        )

        return stage


    async def delete(
        self,
        guild: discord.Guild,
        stage_id: int
    ):

        try:
            channel = guild.get_channel(stage_id)

            if channel is None:
                channel = await guild.fetch_channel(stage_id)

            if channel:
                await channel.delete(reason="Carry Ended")

        except discord.NotFound:
            pass


    async def sync_permissions(
        self,
        guild: discord.Guild,
        carry_id: str
    ):
        return


stage_manager = StageManager()
