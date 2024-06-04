import sqlite3
import os

class XPDatabase:
    def __init__(self, db_path='databases/xp_data.db'):
        self.db_path = db_path
        self.ensure_directory_exists()
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def ensure_directory_exists(self):
        # Ensure the directory for the file_path exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS xp_data (
                    guild_id TEXT,
                    user_id TEXT,
                    xp INTEGER,
                    level INTEGER,
                    PRIMARY KEY (guild_id, user_id)
                )
            """)

    def add_xp(self, guild_id, user_id, xp):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT xp, level FROM xp_data WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
            row = cur.fetchone()
            if row:
                current_xp, current_level = row
                new_xp = current_xp + xp
                leveled_up = self.check_level_up(new_xp, current_level)
                new_level = current_level + 1 if leveled_up else current_level
                cur.execute("UPDATE xp_data SET xp = ?, level = ? WHERE guild_id = ? AND user_id = ?", (new_xp, new_level, guild_id, user_id))
                return leveled_up
            else:
                cur.execute("INSERT INTO xp_data (guild_id, user_id, xp, level) VALUES (?, ?, ?, ?)", (guild_id, user_id, xp, 1))
                return False

        if leveled_up:
            return new_level  # Return the new level when leveled up
        else:
            return False  # Indicates only XP gained, no level up

    def check_level_up(self, xp, level):
        next_level_xp = (level ** 2) * 100
        return xp >= next_level_xp

    def get_user_data(self, guild_id, user_id):
        cur = self.conn.cursor()
        cur.execute("SELECT xp, level FROM xp_data WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        row = cur.fetchone()
        if row:
            xp, level = row
            return {"xp": xp, "level": level}
        else:
            return {"xp": 0, "level": 1}

    def get_leaderboard(self, guild_id, limit=10):
        cur = self.conn.cursor()
        cur.execute("SELECT user_id, xp, level FROM xp_data WHERE guild_id = ? ORDER BY xp DESC LIMIT ?", (guild_id, limit))
        return cur.fetchall()
