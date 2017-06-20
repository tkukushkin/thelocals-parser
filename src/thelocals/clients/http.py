import aiohttp

from thelocals.utils.cache import async_cache


@async_cache
async def get_pool():
    return aiohttp.ClientSession()
