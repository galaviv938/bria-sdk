# tests/test_rmbg.py

import requests_mock
import pytest

from bria.client import Bria
from bria.constants import REMOVE_BACKGROUND_ENDPOINT
from bria.exceptions import InvalidRequestError


def test_remove_background_sync_success():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            REMOVE_BACKGROUND_ENDPOINT,
            json={
                "status": "COMPLETED",
                "result": {"image_url": "https://example.com/output.png"},
            },
            status_code=200,
        )

        resp = client.rmbg.remove_background("https://example.com/input.png", sync=True)
        assert resp["status"] == "COMPLETED"
        assert resp["result"]["image_url"].endswith("output.png")


def test_remove_background_async_inprogress():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            REMOVE_BACKGROUND_ENDPOINT,
            json={
                "status": "IN_PROGRESS",
                "request_id": "req123",
                "status_url": "https://engine.prod.bria-api.com/v2/status/req123",
            },
            status_code=200,
        )

        resp = client.rmbg.remove_background("https://example.com/input.png", sync=False)
        assert resp["status"] == "IN_PROGRESS"
        assert resp["request_id"] == "req123"


def test_remove_background_invalid_request():
    client = Bria(api_token="fake_token")
