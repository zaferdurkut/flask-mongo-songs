import re
from statistics import mean

from bson import ObjectId
from flask import url_for

from api.dto.list_songs_query_input_model import ListSongsQueryModel
from api.dto.song_input_model import SongInputModel
from api.dto.song_output_model import (
    SongOutputModel,
    ListSongOutputModel,
    LinkSongOutputModel,
    HrefItemModel,
)
from api.dto.song_score_output_model import SongScoreOutputModel
from config.mongo_config import mongo_songs_collection


class SongsManager:
    def __init__(self):
        self.collection = mongo_songs_collection

    def list_songs(self, query: ListSongsQueryModel) -> ListSongOutputModel:
        page = query.page
        page_size = query.page_size
        search_string = query.message
        regex_pattern = re.compile(f"^{search_string}")
        conditions = {
            "$and": [
                {"level": query.level} if query.level is not None else {},
                {
                    "$or": [
                        {"artist": regex_pattern},
                        {"title": regex_pattern},
                    ]
                }
                if search_string is not None
                else {},
            ]
        }

        cursor = (
            self.collection.find(conditions)
            .sort("name")
            .skip(page_size * (page - 1))
            .limit(page_size)
        )
        songs_count = self.collection.count_documents(conditions)

        return ListSongOutputModel(
            songs=[SongOutputModel(**song, id=str(song["_id"])) for song in cursor],
            average_difficulty=self.__get_average_difficulty(),
            links=self.__calculate_song_links(
                page=page, page_size=page_size, songs_count=songs_count
            ),
        )

    def get_song_score_with_id(self, song_id: str) -> SongScoreOutputModel:
        song = self.collection.find_one({"_id": ObjectId(song_id)})
        if song is None:
            return SongScoreOutputModel()
        ratings = song.get("ratings", None)
        if ratings is None:
            return SongScoreOutputModel()
        else:
            return SongScoreOutputModel(
                min=min(ratings), average=mean(ratings), max=max(ratings)
            )

    def add_rating(self, song_id: str, rating: int):
        self.collection.update_one(
            filter={"_id": ObjectId(song_id)},
            update={"$push": {"ratings": rating}},
            upsert=True,
        )

    def create_song(self, song: SongInputModel) -> str:
        return str(self.collection.insert_one(song.dict()).inserted_id)

    def __calculate_song_links(
        self, page: int, page_size: int, songs_count: int
    ) -> LinkSongOutputModel:
        links = LinkSongOutputModel(
            self=HrefItemModel(
                href=url_for(
                    ".list_songs",
                    page=page,
                    page_size=page_size,
                    _external=True,
                )
            ),
            last=HrefItemModel(
                href=url_for(
                    ".list_songs",
                    page=(songs_count // page_size) + 1,
                    page_size=page_size,
                    _external=True,
                )
            ),
        )
        if page > 1:
            links.prev = HrefItemModel(
                href=url_for(
                    ".list_songs", page=page - 1, page_size=page_size, _external=True
                )
            )
        if page - 1 < songs_count // page_size:
            links.next = HrefItemModel(
                href=url_for(
                    ".list_songs", page=page + 1, page_size=page_size, _external=True
                )
            )
        return links

    def __get_average_difficulty(self):
        average_difficulty_result = self.collection.aggregate(
            [{"$group": {"_id": 1, "average_difficulty": {"$avg": "$difficulty"}}}]
        )
        try:
            average_difficult = next(average_difficulty_result)["average_difficulty"]
        except StopIteration:
            average_difficult = None

        return average_difficult
