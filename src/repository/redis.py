from redis import asyncio as aioredis
from redis.asyncio import Redis

from data.config import settings

redis_client: Redis = aioredis.from_url(url=settings.redis_url.unicode_string())
