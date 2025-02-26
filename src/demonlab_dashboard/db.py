import asyncio

import asyncpg
from textual.worker import Worker, get_current_worker

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "your_username",
    "password": "your_password",
    "database": "your_database",
}


class Database:
    """Handles PostgreSQL connections and queries."""

    _pool = None

    @classmethod
    async def connect(cls):
        """Initialize connection pool."""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(**DB_CONFIG)
        return cls._pool

    @classmethod
    async def fetch_users(cls):
        """Fetch user data from the database."""
        pool = await cls.connect()
        async with pool.acquire() as conn:
            return await conn.fetch(
                "SELECT id, username, display_name, status FROM users"
            )

    @classmethod
    async def listen_for_notifications(cls, callback):
        """Listen for PostgreSQL notifications and trigger a callback."""
        pool = await cls.connect()
        async with pool.acquire() as conn:
            await conn.execute(
                "LISTEN user_updates;"
            )  # Assumes a NOTIFY trigger on 'user_updates'
            async for notification in conn.notifications():
                callback(notification.payload)

    @classmethod
    async def close(cls):
        """Close the database connection."""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
