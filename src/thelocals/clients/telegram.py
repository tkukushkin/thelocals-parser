from functools import lru_cache

import aiotg

from thelocals import settings


@lru_cache(1)
def get_bot():
    return aiotg.Bot(settings.TELEGRAM_TOKEN)
