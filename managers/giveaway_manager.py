import random
import string
import time

from database import execute, fetchone, fetchall


class GiveawayManager:

    def __init__(self):
        pass

    # ==========================================================
    # PARSE TIME
    # ==========================================================

    def parse_time(
        self,
        value: str
    ) -> int:

        value = value.strip().lower()

        if len(value) < 2:
            raise ValueError("Invalid time.")

        amount = int(value[:-1])

        unit = value[-1]

        if unit == "s":
            return amount

        if unit == "m":
            return amount * 60

        if unit == "h":
            return amount * 60 * 60

        if unit == "d":
            return amount * 60 * 60 * 24

        raise ValueError("Invalid time unit.")

    # ==========================================================
    # GENERATE GIVEAWAY ID
    # ==========================================================

    def generate_id(self) -> str:

        while True:

            giveaway_id = "".join(

                random.choices(

                    string.ascii_uppercase +
                    string.digits,

                    k=8
                )
            )

            exists = fetchone(

                """
                SELECT giveaway_id

                FROM giveaways

                WHERE giveaway_id = ?
                """,

                (
                    giveaway_id,
                )
            )

            if exists is None:

                return giveaway_id

    # ==========================================================
    # CREATE GIVEAWAY
    # ==========================================================

    def create(

        self,

        guild_id: int,

        channel_id: int,

        host_id: int,

        prize: str,

        winners: int,

        duration: str,

        reroll: str

    ) -> dict:

        created_at = int(time.time())

        ends_at = created_at + self.parse_time(
            duration
        )

        reroll_at = ends_at + self.parse_time(
            reroll
        )

        giveaway_id = self.generate_id()

        execute(

            """
            INSERT INTO giveaways(

                giveaway_id,

                guild_id,

                channel_id,

                message_id,

                host_id,

                prize,

                winner_count,

                role_requirement,

                created_at,

                ends_at,

                reroll_at,

                ended

            )

            VALUES(

                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

            )
            """,

            (

                giveaway_id,

                guild_id,

                channel_id,

                None,

                host_id,

                prize,

                winners,

                None,

                created_at,

                ends_at,

                reroll_at,

                0
            )
        )

        return {

            "id": giveaway_id,

            "guild": guild_id,

            "channel": channel_id,

            "host": host_id,

            "prize": prize,

            "winners": winners,

            "created": created_at,

            "ends": ends_at,

            "reroll": reroll_at
        }
        # ==========================================================
    # JOIN GIVEAWAY
    # ==========================================================

    def join(
        self,
        giveaway_id: str,
        user
    ) -> tuple[bool, str]:

        giveaway = fetchone(
            """
            SELECT *
            FROM giveaways
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

        if giveaway is None:
            return False, "Giveaway not found."

        if giveaway["ended"]:
            return False, "This giveaway has already ended."

        if giveaway["role_requirement"]:

            role = user.guild.get_role(
                giveaway["role_requirement"]
            )

            if role is None:
                return False, "Required role no longer exists."

            if role not in user.roles:
                return False, f"You need {role.mention}."

        exists = fetchone(
            """
            SELECT *
            FROM giveaway_entries
            WHERE giveaway_id = ?
            AND user_id = ?
            """,
            (
                giveaway_id,
                user.id
            )
        )

        if exists:
            return False, "You already joined."

        execute(
            """
            INSERT INTO giveaway_entries(

                giveaway_id,

                user_id,

                joined_at

            )

            VALUES(

                ?, ?, ?

            )
            """,
            (
                giveaway_id,
                user.id,
                int(time.time())
            )
        )

        return True, "Joined successfully."

    # ==========================================================
    # LEAVE GIVEAWAY
    # ==========================================================

    def leave(
        self,
        giveaway_id: str,
        user_id: int
    ) -> tuple[bool, str]:

        exists = fetchone(
            """
            SELECT *
            FROM giveaway_entries
            WHERE giveaway_id = ?
            AND user_id = ?
            """,
            (
                giveaway_id,
                user_id
            )
        )

        if exists is None:
            return False, "You are not entered."

        execute(
            """
            DELETE FROM giveaway_entries
            WHERE giveaway_id = ?
            AND user_id = ?
            """,
            (
                giveaway_id,
                user_id
            )
        )

        return True, "Successfully left."

    # ==========================================================
    # ENTRY COUNT
    # ==========================================================

    def entry_count(
        self,
        giveaway_id: str
    ) -> int:

        result = fetchone(
            """
            SELECT COUNT(*) AS total
            FROM giveaway_entries
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

        return result["total"]

    # ==========================================================
    # PICK WINNERS
    # ==========================================================

    def pick_winners(
        self,
        giveaway_id: str
    ) -> list[int]:

        giveaway = fetchone(
            """
            SELECT *
            FROM giveaways
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

        if giveaway is None:
            return []

        entries = fetchall(
            """
            SELECT user_id
            FROM giveaway_entries
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

        users = [row["user_id"] for row in entries]

        if not users:
            return []

        winner_count = min(
            giveaway["winner_count"],
            len(users)
        )

        return random.sample(
            users,
            winner_count
        )
        # ==========================================================
    # END GIVEAWAY
    # ==========================================================

    def end_giveaway(
        self,
        giveaway_id: str
    ) -> list[int]:

        winners = self.pick_winners(
            giveaway_id
        )

        execute(
            """
            UPDATE giveaways
            SET ended = 1
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

        execute(
            """
            DELETE FROM giveaway_winners
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

        for user_id in winners:

            execute(
                """
                INSERT INTO giveaway_winners(

                    giveaway_id,

                    user_id,

                    won_at

                )

                VALUES(

                    ?, ?, ?

                )
                """,
                (
                    giveaway_id,
                    user_id,
                    int(time.time())
                )
            )

        return winners

    # ==========================================================
    # REROLL GIVEAWAY
    # ==========================================================

    def reroll_giveaway(
        self,
        giveaway_id: str
    ) -> list[int]:

        execute(
            """
            DELETE FROM giveaway_winners
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

        winners = self.pick_winners(
            giveaway_id
        )

        for user_id in winners:

            execute(
                """
                INSERT INTO giveaway_winners(

                    giveaway_id,

                    user_id,

                    won_at

                )

                VALUES(

                    ?, ?, ?

                )
                """,
                (
                    giveaway_id,
                    user_id,
                    int(time.time())
                )
            )

        return winners

    # ==========================================================
    # GET GIVEAWAY
    # ==========================================================

    def get(
        self,
        giveaway_id: str
    ):

        return fetchone(
            """
            SELECT *
            FROM giveaways
            WHERE giveaway_id = ?
            """,
            (
                giveaway_id,
            )
        )

    # ==========================================================
    # UPDATE MESSAGE ID
    # ==========================================================

    def set_message(
        self,
        giveaway_id: str,
        message_id: int
    ):

        execute(
            """
            UPDATE giveaways
            SET message_id = ?
            WHERE giveaway_id = ?
            """,
            (
                message_id,
                giveaway_id
            )
        )

    # ==========================================================
    # ACTIVE GIVEAWAYS
    # ==========================================================

    def active(self):

        return fetchall(
            """
            SELECT *
            FROM giveaways
            WHERE ended = 0
            """
        )

    # ==========================================================
    # EXPIRED GIVEAWAYS
    # ==========================================================

    def expired(self):

        now = int(time.time())

        return fetchall(
            """
            SELECT *
            FROM giveaways
            WHERE ended = 0
            AND ends_at <= ?
            """,
            (
                now,
            )
        )
