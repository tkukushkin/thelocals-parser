from thelocals import settings
from thelocals.models import User, Kind, Coordinates


def mget_all():
    return [_map_user_from_dict(user_data) for user_data in settings.USERS]


def _map_user_from_dict(data):
    kwarks = data.copy()
    kwarks['kind'] = data['kind'] and Kind(data['kind'])
    kwarks['work_coordinates'] = Coordinates(
        lat=data['work_coordinates']['lat'],
        lng=data['work_coordinates']['lng'],
    )
    return User(**kwarks)
