import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from thelocals import settings
from thelocals.clients import http
from thelocals.models import Coordinates


class Mode(Enum):
    transit = 'transit'
    walking = 'walking'


async def get_time(origin: Coordinates, destination: Coordinates, mode: Mode) -> Optional[int]:
    pool = await http.get_pool()
    departure_time = datetime.now().replace(hour=9, minute=30) + timedelta(days=1)
    response = await pool.get('https://maps.googleapis.com/maps/api/directions/json', params={
        'key': settings.GOOGLE_API_KEY,
        'origin': '{},{}'.format(origin.lat, origin.lng),
        'destination': '{},{}'.format(destination.lat, destination.lng),
        'departure_time': int(time.mktime(departure_time.timetuple())),
        'mode': mode.value,
        'language': 'ru',
    })
    data = await response.json()
    if not data['routes']:
        return None
    return data['routes'][0]['legs'][0]['duration']['value']
