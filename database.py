import sqlite3
from typing import List, Optional, Tuple


class Database:
    def __init__(self, db_name: str = "weather_bot.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        print(" DB connected")

    def create_tables(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )

        self.conn.commit()
        print("Tables created")

    def add_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
    ):
        try:
            self.cur.execute(
                "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                (user_id, username, first_name),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error users adding: {e}")

    def add_address(self, user_id: int, address: str):
        try:
            self.cur.execute(
                "INSERT INTO user_addresses (user_id, address) VALUES (?, ?)",
                (user_id, address),
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error address adding: {e}")
            return False

    def get_user_addresses(self, user_id: int) -> List[Tuple]:
        self.cur.execute(
            "SELECT id, address, created_at FROM user_addresses WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return self.cur.fetchall()

    def delete_users_addresses(self, address_id: int, user_id: int) -> bool:
        try:
            self.cur.execute(
                "DELETE FROM user_addresses WHERE id = ? AND user_id = ?",
                (address_id, user_id),
            )
            self.conn.commit()
            return self.cur.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting address: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()
            print("DB connection successfully closed")


db = Database()
