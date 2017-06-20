import asyncio
import logging

from thelocals.clients import http, redis


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)-15s %(levelname)s %(name)s: %(message)s'
    )


def setup():
    setup_logging()


def teardown():
    loop = asyncio.get_event_loop()
    for client in [http, redis]:
        if client.get_pool.cache:
            loop.run_until_complete(client.get_pool()).close()
