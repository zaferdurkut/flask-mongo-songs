from datetime import date

from pydantic import BaseModel


class CreateSongOutputModel(BaseModel):
    id: str
