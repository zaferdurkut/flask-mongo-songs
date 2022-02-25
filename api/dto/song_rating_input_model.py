from pydantic import BaseModel, conint


class SongRatingInputModel(BaseModel):
    rating: conint(ge=1, le=5)
