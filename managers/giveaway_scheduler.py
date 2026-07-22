import asyncio
import random

import discord
from discord.ext import tasks

from database import fetchall, execute


class GiveawayScheduler:

    def __init__(self, bot):

        self.bot = bot

        self.loop.start()


    @tasks.loop(seconds=30)
    async def loop(self):

        giveaways = fetchall(
            """
            SELECT *
            FROM giveaways
            WHERE ended = 0
            """
        )

        now = int(discord.utils.utcnow().timestamp())

        for giveaway in giveaways:

            if giveaway["ends_at"] <= now:

                await self.finish(
                    giveaway
                )


    @loop.before_loop
    async def before_loop(self):

        await self.bot.wait_until_ready()
            async def finish(self, giveaway):

        entries = fetchall(
            """
            SELECT user_id
            FROM giveaway_entries
            WHERE giveaway_id = ?
            """,
            (
                giveaway["giveaway_id"],
            )
        )

        users = [
            row["user_id"]
            for row in entries
        ]

        if len(users) == 0:

            execute(
                """
                UPDATE giveaways
                SET ended = 1
                WHERE giveaway_id = ?
                """,
                (
                    giveaway["giveaway_id"],
                )
            )

            return

        winner_count = min(
            giveaway["winner_count"],
            len(users)
        )

        winners = random.sample(
            users,
            winner_count
        )

        for winner in winners:

            execute(
                """
                INSERT OR REPLACE
                INTO giveaway_winners
                VALUES
                (?, ?, 0, NULL)
                """,
                (
                    giveaway["giveaway_id"],
                    winner
                )
            )

        execute(
            """
            UPDATE giveaways
            SET ended = 1
            WHERE giveaway_id = ?
            """,
            (
                giveaway["giveaway_id"],
            )
        )

        await self.send_winner_dms(
            giveaway,
            winners
        )
            async def send_winner_dms(
        self,
        giveaway,
        winners
    ):

        from views.giveaway_claim_view import GiveawayClaimView

        channel = self.bot.get_channel(
            giveaway["channel_id"]
        )

        jump_url = None

        if (
            channel is not None
            and giveaway["message_id"]
        ):

            try:

                message = await channel.fetch_message(
                    giveaway["message_id"]
                )

                jump_url = message.jump_url

            except Exception:
                message = None

        else:
            message = None

        for user_id in winners:

            user = self.bot.get_user(user_id)

            if user is None:

                try:
                    user = await self.bot.fetch_user(user_id)

                except Exception:
                    continue

            embed = discord.Embed(
                title="🎉 Congratulations!",
                color=discord.Color.green()
            )

            embed.add_field(
                name="Prize",
                value=giveaway["prize"],
                inline=False
            )

            embed.add_field(
                name="Giveaway ID",
                value=giveaway["giveaway_id"],
                inline=False
            )

            if jump_url:

                embed.add_field(
                    name="Original Giveaway",
                    value=jump_url,
                    inline=False
                )

            try:

                await user.send(
                    embed=embed,
                    view=GiveawayClaimView(
                        giveaway["giveaway_id"]
                    )
                )

            except Exception:
                pass

        if message:

            await message.add_reaction("✅")
                @tasks.loop(seconds=60)
    async def reroll_loop(self):

        now = int(discord.utils.utcnow().timestamp())

        giveaways = fetchall(
            """
            SELECT *
            FROM giveaways
            WHERE ended = 1
            """
        )

        for giveaway in giveaways:

            reroll = fetchone(
                """
                SELECT *
                FROM giveaway_rerolls
                WHERE giveaway_id = ?
                """,
                (
                    giveaway["giveaway_id"],
                )
            )

            if reroll is not None:
                continue

            if giveaway["reroll_at"] > now:
                continue

            winners = fetchall(
                """
                SELECT *
                FROM giveaway_winners
                WHERE giveaway_id = ?
                AND claimed = 0
                """,
                (
                    giveaway["giveaway_id"],
                )
            )

            if len(winners) == 0:

                execute(
                    """
                    INSERT INTO giveaway_rerolls
                    VALUES (?, 1, ?)
                    """,
                    (
                        giveaway["giveaway_id"],
                        now
                    )
                )

                continue

            await self.reroll(
                giveaway
            )


    @reroll_loop.before_loop
    async def before_reroll_loop(self):

        await self.bot.wait_until_ready()
        
