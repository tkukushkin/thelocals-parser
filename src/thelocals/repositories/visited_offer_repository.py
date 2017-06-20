from thelocals.clients import redis


async def mget_all():
    pool = await redis.get_pool()
    result = await pool.lrange_aslist('offers')
    return {int(item) for item in result}


async def add(id: int):
    pool = await redis.get_pool()
    await pool.rpush('offers', [str(id)])
