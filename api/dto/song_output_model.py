from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class HrefItemModel(BaseModel):
    href: str


class SongOutputModel(BaseModel):
    id: str
    artist: str
    title: str
    difficulty: float
    level: int
    released: date


class LinkSongOutputModel(BaseModel):
    self: Optional[HrefItemModel]
    last: Optional[HrefItemModel]
    next: Optional[HrefItemModel]
    prev: Optional[HrefItemModel]


class ListSongOutputModel(BaseModel):
    songs: List[SongOutputModel]
    links: LinkSongOutputModel
    average_difficulty: Optional[float]
