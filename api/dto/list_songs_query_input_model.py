from typing import Optional

from pydantic import BaseModel


class ListSongsQueryModel(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 25
    level: Optional[int]
    message: Optional[str]
