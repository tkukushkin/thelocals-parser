import logging
from typing import List
from urllib.parse import urljoin

from thelocals.clients.http import get_pool
from thelocals.models import Kind, MapOffer, Offer


logger = logging.getLogger(__name__)


async def mget_all() -> List[Offer]:
    pool = await get_pool()
    response = await pool.get('https://thelocals.ru/api/frontend/rooms/map')
    data = await response.json()
    return [
        MapOffer(
            id=obj['id'],
            lat=obj['lat'],
            lng=obj['lng'],
            address=obj['address'],
            rooms=obj['rooms'] if obj['rooms'] != 'K' else None,
            kind=Kind.apartment if obj['rooms'] != 'K' else Kind.room,
        )
        for obj in data['ads']
    ]


async def get(id: int) -> Offer:
    pool = await get_pool()
    response = await pool.get('https://thelocals.ru/api/frontend/rooms/{}'.format(id))
    data = await response.json()

    return Offer(
        id=data['id'],
        lat=data['lat'],
        lng=data['lng'],
        address=data['address'],
        rooms=data['rooms'] if data['rooms'] != 'K' else None,
        kind=Kind.apartment if data['rooms'] != 'K' else Kind.room,
        title=data['title'],
        url=urljoin('https://thelocals.ru/', data['path']),
        price=_to_int(data.get('price')),
        square=_to_int(data.get('space')),
        image=data['image'],
    )


def _to_int(s):
    try:
        return int(''.join(filter(str.isdigit, s or '')))
    except ValueError:
        return None
