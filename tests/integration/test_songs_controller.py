import json
from statistics import mean

import pytest
from bson import ObjectId
from requests import Response

from api.dto.list_songs_query_input_model import ListSongsQueryModel
from api.dto.song_input_model import SongInputModel
from api.dto.song_output_model import SongOutputModel
from api.dto.song_rating_input_model import SongRatingInputModel
from api.dto.song_score_output_model import SongScoreOutputModel
from app import create_app
from config.mongo_config import mongo_songs_collection
from tests.constants import (
    INITIAL_SONGS_PATH,
    SONGS_BASE_PATH,
    SONGS_RATING_PATH,
    SONGS_SCORE_PATH,
)
from tests.integration.expected_responses import (
    LIST_SONG_EXPECTED_FULL_DATA_WITHOUT_IDS,
    LIST_SONG_EXPECTED_PAGING_DATA,
)


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    mongo_songs_collection.drop()

    yield app

    mongo_songs_collection.drop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class TestSongsController:
    @staticmethod
    def test_should_initialize_songs(client):
        # given

        # when
        response: Response = client.get(
            INITIAL_SONGS_PATH,
        )
        # then
        assert response.status_code == 204
        songs_count = mongo_songs_collection.count_documents({})
        assert songs_count == 11

    @staticmethod
    def test_should_list_songs(client):
        # when
        initial_songs_response: Response = client.get(
            INITIAL_SONGS_PATH,
        )
        # then
        assert initial_songs_response.status_code == 204

        ## full data control
        # given
        params = ListSongsQueryModel(page=1, page_size=15, level=None, message=None)

        # when
        list_songs_response: Response = client.get(
            SONGS_BASE_PATH, query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        for song in response_data["songs"]:
            song.pop("id", None)
        assert response_data == LIST_SONG_EXPECTED_FULL_DATA_WITHOUT_IDS

        ## paging and links control
        # given
        params = ListSongsQueryModel(page=2, page_size=4, level=None, message=None)

        # when
        list_songs_response: Response = client.get(
            SONGS_BASE_PATH, query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        assert len(response_data["songs"]) == 4
        assert response_data["links"] == LIST_SONG_EXPECTED_PAGING_DATA

        ## irrelevant page control
        # given
        params = ListSongsQueryModel(page=100, page_size=4, level=None, message=None)

        # when
        list_songs_response: Response = client.get(
            SONGS_BASE_PATH, query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        assert len(response_data["songs"]) == 0

        ## level control
        # given
        params = ListSongsQueryModel(page=1, page_size=4, level=9, message=None)

        # when
        list_songs_response: Response = client.get(
            SONGS_BASE_PATH, query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        assert len(response_data["songs"]) == 3

        ## search string control with title
        # given
        params = ListSongsQueryModel(page=1, page_size=4, level=None, message="Vivaldi")

        # when
        list_songs_response: Response = client.get(
            SONGS_BASE_PATH, query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        assert len(response_data["songs"]) == 1

        ## search string control with artist
        # given
        params = ListSongsQueryModel(
            page=1, page_size=4, level=None, message="Mr Fastfinger"
        )

        # when
        list_songs_response: Response = client.get(
            SONGS_BASE_PATH, query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        assert len(response_data["songs"]) == 1

        ## search string control with artist and title
        # given
        params = ListSongsQueryModel(page=1, page_size=10, level=None, message="The")

        # when
        list_songs_response: Response = client.get(
            SONGS_BASE_PATH, query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        assert len(response_data["songs"]) == 10

    @staticmethod
    def test_should_add_song(client):
        # given
        input_model = SongInputModel(
            artist="The Test Artist",
            title="The Test Title",
            difficulty=10.1123,
            level=5,
            released="2022-02-24",
        )

        # when
        create_songs_response: Response = client.post(
            SONGS_BASE_PATH, data=input_model.json(), content_type="application/json"
        )

        # then
        assert create_songs_response.status_code == 200
        song_id = json.loads(create_songs_response.get_data(as_text=True))["id"]
        song = mongo_songs_collection.find_one({"_id": ObjectId(song_id)})
        assert (
            SongOutputModel(**song, id=str(song["_id"])).json(exclude={"id", "rating"})
            == input_model.json()
        )

    @staticmethod
    def test_should_add_rating_and_get_score(client):
        ## Add song
        # given
        input_model = SongInputModel(
            artist="The Test Artist",
            title="The Test Title",
            difficulty=10.1123,
            level=5,
            released="2022-02-24",
        )
        # when
        create_songs_response: Response = client.post(
            SONGS_BASE_PATH, data=input_model.json(), content_type="application/json"
        )

        # then
        assert create_songs_response.status_code == 200
        song_id = json.loads(create_songs_response.get_data(as_text=True))["id"]

        ## Add rating
        # given
        ratings = [1, 1, 2, 2, 3, 3, 5, 5, 4]
        for item in ratings:
            input_model = SongRatingInputModel(rating=item)
            # when
            add_rating_response: Response = client.put(
                SONGS_RATING_PATH.format(song_id=song_id),
                data=input_model.json(),
                content_type="application/json",
            )
            # then
            assert add_rating_response.status_code == 204

        ## get score
        # given
        params = ListSongsQueryModel(page=1, page_size=10, level=None, message="The")

        # when
        list_songs_response: Response = client.get(
            SONGS_SCORE_PATH.format(song_id=song_id), query_string=params.dict()
        )

        # then
        assert list_songs_response.status_code == 200
        response_data = json.loads(list_songs_response.get_data(as_text=True))
        assert (
            response_data
            == SongScoreOutputModel(
                min=min(ratings), max=max(ratings), average=mean(ratings)
            ).dict()
        )
