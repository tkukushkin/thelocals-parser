from enum import Enum
from typing import NamedTuple, Optional


class Kind(Enum):
    apartment = 'apartment'
    room = 'room'


class Coordinates(NamedTuple):
    lat: float
    lng: float


class MapOffer(NamedTuple):
    id: int
    lat: float
    lng: float
    address: str
    kind: Kind
    rooms: Optional[int]


class Offer(NamedTuple):
    id: int
    lat: float
    lng: float
    address: str
    kind: Kind
    rooms: Optional[int]
    title: str
    url: str
    square: Optional[int]
    price: Optional[int]
    image: Optional[str]

    @property
    def coordinates(self) -> Coordinates:
        return Coordinates(lat=self.lat, lng=self.lng)


class User(NamedTuple):
    id: int
    kind: Kind
    rooms: Optional[int]
    min_price: Optional[int]
    max_price: Optional[int]
    max_time_to_subway: int
    work_coordinates: Coordinates
    max_time_to_work: Optional[int]


class Subway(NamedTuple):
    coordinates: Coordinates
    name: str
