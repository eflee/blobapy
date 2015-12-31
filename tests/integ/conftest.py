import json
import pytest
from blobapy import app


@pytest.fixture
def test_client():
    return app.app.test_client()


@pytest.fixture
def call(test_client):
    def _call(url, data=None):
        if data is not None:
            response = test_client.post(url, data=data)
        else:
            response = test_client.get(url)
        return json.loads(response.data.decode("utf-8"))
    return _call
