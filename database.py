import sqlite3
from pathlib import Path

# --------------------
# PATHS
# --------------------

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(exist_ok=True)

DB_PATH = DATA_FOLDER / "carrybot.db"

# --------------------
# CONNECTION
# --------------------

connection = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# --------------------
# HELPERS
# --------------------

def execute(query: str, params=()):
    cursor.execute(query, params)
    connection.commit()
    return cursor


def fetchone(query: str, params=()):
    return cursor.execute(query, params).fetchone()


def fetchall(query: str, params=()):
    return cursor.execute(query, params).fetchall()


# --------------------
# CREATE TABLES
# --------------------

def create_tables():

    # ====================
    # CARRIES
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carries(

        carry_id TEXT PRIMARY KEY,

        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,

        message_id INTEGER,
        stage_id INTEGER,

        role_id INTEGER,

        host_id INTEGER NOT NULL,

        boss TEXT NOT NULL,

        max_players INTEGER NOT NULL,

        active TEXT NOT NULL,

        waiting TEXT NOT NULL,

        scheduled INTEGER DEFAULT 0,

        scheduled_for INTEGER,

        created INTEGER NOT NULL,

        finished INTEGER DEFAULT 0
    )
    """)

    # ====================
    # CARRY LOGS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carry_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        carry_id TEXT NOT NULL,

        user_id INTEGER NOT NULL,

        action TEXT NOT NULL,

        timestamp INTEGER NOT NULL
    )
    """)

    connection.commit()
        # ====================
    # PERSONAL BLACKLIST
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personal_blacklist(

        host_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        reason TEXT,

        added_by INTEGER,

        added_at INTEGER,

        PRIMARY KEY(host_id, user_id)
    )
    """)

    # ====================
    # GLOBAL BLACKLIST
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS global_blacklist(

        user_id INTEGER PRIMARY KEY,

        reason TEXT,

        added_by INTEGER NOT NULL,

        added_at INTEGER NOT NULL
    )
    """)

    # ====================
    # WARNS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warns(

        warn_id INTEGER PRIMARY KEY AUTOINCREMENT,

        guild_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        moderator_id INTEGER NOT NULL,

        reason TEXT,

        created INTEGER NOT NULL
    )
    """)

    # ====================
    # MODERATION ACTIONS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS moderation_actions(

        action_id INTEGER PRIMARY KEY AUTOINCREMENT,

        guild_id INTEGER NOT NULL,

        moderator_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        action TEXT NOT NULL,

        duration INTEGER,

        reason TEXT,

        created INTEGER NOT NULL
    )
    """)

    # ====================
    # SUSPICION USERS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suspicion_users(

        user_id INTEGER PRIMARY KEY,

        reason TEXT,

        added_by INTEGER,

        added_at INTEGER
    )
    """)

    connection.commit()
        # ====================
    # GIVEAWAYS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS giveaways(

        giveaway_id TEXT PRIMARY KEY,

        guild_id INTEGER NOT NULL,

        channel_id INTEGER NOT NULL,

        message_id INTEGER,

        host_id INTEGER NOT NULL,

        prize TEXT NOT NULL,

        winner_count INTEGER NOT NULL,

        role_requirement INTEGER,

        created_at INTEGER NOT NULL,

        ends_at INTEGER NOT NULL,

        reroll_at INTEGER NOT NULL,

        ended INTEGER DEFAULT 0
    )
    """)

    # ====================
    # GIVEAWAY ENTRIES
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS giveaway_entries(

        giveaway_id TEXT NOT NULL,

        user_id INTEGER NOT NULL,

        joined_at INTEGER NOT NULL,

        PRIMARY KEY(giveaway_id, user_id)
    )
    """)

    # ====================
    # GIVEAWAY WINNERS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS giveaway_winners(

        giveaway_id TEXT NOT NULL,

        user_id INTEGER NOT NULL,

        claimed INTEGER DEFAULT 0,

        claimed_at INTEGER,

        PRIMARY KEY(giveaway_id, user_id)
    )
    """)

    # ====================
    # GIVEAWAY REROLLS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS giveaway_rerolls(

        giveaway_id TEXT PRIMARY KEY,

        rerolled INTEGER DEFAULT 0,

        rerolled_at INTEGER
    )
    """)

    connection.commit()
        # ====================
    # TICKETS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(

        ticket_id TEXT PRIMARY KEY,

        guild_id INTEGER NOT NULL,

        channel_id INTEGER NOT NULL,

        creator_id INTEGER NOT NULL,

        type TEXT NOT NULL,

        created_at INTEGER NOT NULL,

        closed INTEGER DEFAULT 0,

        closed_by INTEGER,

        closed_at INTEGER
    )
    """)

    # ====================
    # INCIDENT REPORTS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incident_reports(

        incident_id TEXT PRIMARY KEY,

        carry_id TEXT NOT NULL,

        ticket_id TEXT,

        host_id INTEGER NOT NULL,

        moderator_id INTEGER,

        action TEXT,

        resolution TEXT,

        created_at INTEGER NOT NULL,

        resolved_at INTEGER
    )
    """)

    # ====================
    # HOSTER APPLICATIONS
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hoster_applications(

        application_id TEXT PRIMARY KEY,

        guild_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        region TEXT NOT NULL,

        clip_link TEXT NOT NULL,

        status TEXT NOT NULL,

        reviewer_id INTEGER,

        created_at INTEGER NOT NULL,

        reviewed_at INTEGER
    )
    """)

    # ====================
    # VOUCHES
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vouches(

        host_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        created_at INTEGER NOT NULL,

        PRIMARY KEY(host_id, user_id)
    )
    """)

    # ====================
    # LEADERBOARD CACHE
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leaderboard(

        host_id INTEGER PRIMARY KEY,

        vouches INTEGER DEFAULT 0,

        carries INTEGER DEFAULT 0,

        players INTEGER DEFAULT 0,

        updated_at INTEGER
    )
    """)

    # ====================
    # SCHEDULED CARRIES
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scheduled_carries(

        carry_id TEXT PRIMARY KEY,

        start_at INTEGER NOT NULL,

        reminder_sent INTEGER DEFAULT 0
    )
    """)

    # ====================
    # GUILD CONFIG
    # ====================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guild_config(

        guild_id INTEGER PRIMARY KEY,

        setup_completed INTEGER DEFAULT 0,

        giveaway_channel_id INTEGER,
        giveaway_role_id INTEGER,

        moderation_log_channel_id INTEGER,

        ticket_panel_channel_id INTEGER,

        incident_log_channel_id INTEGER,

        leaderboard_channel_id INTEGER,

        hoster_application_channel_id INTEGER
    )
    """)

    connection.commit()
        # ====================
    # INDEXES
    # ====================

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_carry_logs_carry
    ON carry_logs(carry_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_warns_user
    ON warns(user_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_mod_actions_user
    ON moderation_actions(user_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_entries_giveaway
    ON giveaway_entries(giveaway_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_vouches_host
    ON vouches(host_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_tickets_creator
    ON tickets(creator_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_incidents_host
    ON incident_reports(host_id)
    """)

    connection.commit()
db=connection
