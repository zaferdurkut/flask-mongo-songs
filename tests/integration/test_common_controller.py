import json
from unittest import TestCase

import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


COMMON_PATH = "/api/common/"


class CommonController(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = client(self.app)

    def test_common(self):
        response = self.client.get(COMMON_PATH)

        assert response.status_code == 200

        response_data = json.loads(response.data)
        assert response_data == {"status": True}
