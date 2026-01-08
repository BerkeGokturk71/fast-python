from redis.asyncio import Redis

class RedisClient:
    _client: Redis | None = None

    @classmethod
    async def connect(cls):
        if cls._client is None:
            cls._client = Redis(
                host="localhost",
                port=6379,
                decode_responses=True
            )
            await cls._client.ping()  # 🔥 Redis ayakta mı test et

    @classmethod
    def get(cls) -> Redis:
        if cls._client is None:
            raise RuntimeError("Redis not initialized")
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None
