import asyncio
import logging
from datetime import timedelta
from typing import List

from thelocals.clients.telegram import get_bot
from thelocals.models import Offer, User, Subway
from thelocals.repositories import (
    google_route_repository,
    google_subway_repository,
    thelocals_offer_repository,
    user_repository,
    visited_offer_repository,
)


logger = logging.getLogger(__name__)


async def search_by_interval(interval: timedelta):
    while True:
        logger.info('Parsing new offers...')
        await _search()
        await asyncio.sleep(interval.total_seconds())


async def _search() -> None:
    map_offers = await thelocals_offer_repository.mget_all()

    visited_ids = await visited_offer_repository.mget_all()

    ids = [offer.id for offer in map_offers if offer.id not in visited_ids]

    offers = await asyncio.gather(*[
        thelocals_offer_repository.get(id)
        for id in ids
    ])

    users = user_repository.mget_all()

    for offer in offers:
        await _process_offer(offer, users)
        await visited_offer_repository.add(offer.id)


async def _process_offer(offer: Offer, users: List[User]) -> None:
    subways = await google_subway_repository.mget_nearest(offer.coordinates)
    if not subways:
        return

    subway, time_to_subway = min([
        (
            subway,
            await google_route_repository.get_time(
                origin=offer.coordinates,
                destination=subway.coordinates,
                mode=google_route_repository.Mode.walking,
            )
        )
        for subway in subways[:2]
    ], key=lambda p: p[1] or float('+inf'))

    for user in users:
        if offer.kind != user.kind:
            continue
        if offer.rooms != user.rooms:
            continue
        if offer.price > user.max_price or offer.price < user.min_price:
            continue
        if not time_to_subway or time_to_subway / 60 > user.max_time_to_subway:
            continue

        time_to_work = await google_route_repository.get_time(
            origin=offer.coordinates,
            destination=user.work_coordinates,
            mode=google_route_repository.Mode.transit,
        )

        if not time_to_work or time_to_work / 60 > user.max_time_to_work:
            continue

        await _send_offer(offer, user, subway, time_to_subway, time_to_work)


async def _send_offer(offer: Offer, user: User, subway: Subway, time_to_subway: int, time_to_work: int) -> None:
    lines = [
        '[{}]({})'.format(offer.title, offer.url),
        'Адрес: {}'.format(offer.address),
        'Цена: {}'.format(offer.price),
        'Время до ближайшей станции метро ({}): {} мин.'.format(subway.name, time_to_subway // 60),
        'Время до работы: {} мин.'.format(time_to_work // 60),
    ]
    bot = get_bot()
    chat = bot.private(user.id)
    await chat.send_text('\n'.join(lines), parse_mode='Markdown')
