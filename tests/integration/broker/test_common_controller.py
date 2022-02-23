import json
from unittest import TestCase

from flask.testing import FlaskClient

from run import app

client = app.test_client()

COMMON_PATH = "/api/common/"


class CommonController(TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = FlaskClient(self.app)

    def test_common(self):
        response = client.get(COMMON_PATH)

        assert response.status_code == 200

        response_data = json.loads(response.data)
        assert response_data == {"status": True}
