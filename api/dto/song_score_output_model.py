from typing import Optional

from pydantic import BaseModel


class SongScoreOutputModel(BaseModel):
    min: Optional[int]
    average: Optional[float]
    max: Optional[int]
