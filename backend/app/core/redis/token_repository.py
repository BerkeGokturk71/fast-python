from backend.app.core.redis.ttl import ACCESS_TOKEN_TTL, REFRESH_TOKEN_TTL
from backend.app.core.redis.keys import RedisKeys
from backend.app.core.redis.client import RedisClient

class TokenRepository:

    def __init__(self):
        self.redis = RedisClient.get()

    async def store_access(self, jti: str, user_id: int):
        await self.redis.setex(
            RedisKeys.access(jti),
            ACCESS_TOKEN_TTL,
            user_id
        )

    async def store_refresh(self, jti: str, user_id: int):
        await self.redis.setex(
            RedisKeys.refresh(jti),
            REFRESH_TOKEN_TTL,
            user_id
        )

    async def is_access_valid(self, jti: str) -> bool:
        return await self.redis.exists(RedisKeys.access(jti))

    async def get_refresh_user(self, jti: str) -> int | None:
        return await self.redis.get(RedisKeys.refresh(jti))

    async def revoke_access(self, jti: str):
        await self.redis.delete(RedisKeys.access(jti))

    async def revoke_refresh(self, jti: str):
        await self.redis.delete(RedisKeys.refresh(jti))
