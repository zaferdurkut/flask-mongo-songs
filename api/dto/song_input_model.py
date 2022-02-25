from pydantic import BaseModel


class SongInputModel(BaseModel):
    artist: str
    title: str
    difficulty: float
    level: int
    released: str
