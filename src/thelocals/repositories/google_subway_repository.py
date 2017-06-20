from typing import List

from thelocals import settings
from thelocals.clients import http
from thelocals.models import Coordinates, Subway


async def mget_nearest(coordinates: Coordinates) -> List[Subway]:
    pool = await http.get_pool()
    response = await pool.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params={
        'key': settings.GOOGLE_API_KEY,
        'location': '{},{}'.format(coordinates.lat, coordinates.lng),
        'rankby': 'distance',
        'type': 'subway_station',
        'language': 'ru',
    })
    data = await response.json()
    return [
        Subway(
            name=subway_data['name'],
            coordinates=Coordinates(
                lat=subway_data['geometry']['location']['lat'],
                lng=subway_data['geometry']['location']['lng'],
            ),
        )
        for subway_data in data['results']
    ]
