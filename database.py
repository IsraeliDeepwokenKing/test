import sqlite3
import os


DB_FOLDER = "data"
DB_PATH = os.path.join(DB_FOLDER, "carrybot.db")

os.makedirs(DB_FOLDER, exist_ok=True)


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS carries(

            carry_id TEXT PRIMARY KEY,

            guild_id INTEGER,

            host_id INTEGER,

            boss TEXT,

            max_players INTEGER,

            stage_id INTEGER,

            message_id INTEGER,

            channel_id INTEGER,

            role_id INTEGER,

            active TEXT,

            waiting TEXT,

            created INTEGER

        )

        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS blacklist(

            host_id INTEGER,

            player_id INTEGER

        )

        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS carry_logs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            carry_id TEXT NOT NULL,

            user_id INTEGER NOT NULL,

            action TEXT NOT NULL,

            timestamp INTEGER NOT NULL

        )

        """)

        self.conn.commit()


db = Database()
