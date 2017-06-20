import asyncio_redis

from thelocals import settings
from thelocals.utils.cache import async_cache


@async_cache
async def get_pool():
    return await asyncio_redis.Pool.create(**settings.REDIS_CONNECTION_PARAMS)
