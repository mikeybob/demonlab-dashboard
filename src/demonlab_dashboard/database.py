import asyncpg

DB_CONFIG = {
    "host": "10.99.10.128",
    "port": 5432,
    "user": "synapse_user",
    "password": "synapse",
    "database": "synapse",
}

class Database:
    _pool = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(**DB_CONFIG)
        return cls._pool

    @classmethod
    async def execute_query(cls, query):
        pool = await cls.connect()
        async with pool.acquire() as conn:
            return await conn.fetch(query)

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
