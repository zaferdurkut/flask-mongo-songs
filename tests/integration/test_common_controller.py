import pytest
from requests import Response

from app import create_app
from config.mongo_config import mongo_songs_collection
from tests.constants import INITIAL_SONGS_PATH, COMMON_PATH


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


class TestCommonController:
    @staticmethod
    def test_should_get_healthy(client):
        # given

        # when
        response: Response = client.get(
            INITIAL_SONGS_PATH,
        )
        # then
        assert response.status_code == 204
