import requests_mock
import pytest

from src.bria.client import Bria
from src.bria.constants import (
    REMOVE_BACKGROUND_ENDPOINT,
    RESULT_KEY,
    IMAGE_URL_KEY,
    STATUS_KEY,
    REQUEST_ID_KEY,
    STATUS_URL_KEY,
)
from src.bria.exceptions import InvalidRequestError
from src.bria.models import RemoveBackgroundResult


def test_remove_background_sync_success():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            REMOVE_BACKGROUND_ENDPOINT,
            json={
                STATUS_KEY: "COMPLETED",
                RESULT_KEY: {IMAGE_URL_KEY: "https://example.com/output.png"},
            },
            status_code=200,
        )

        resp = client.rmbg.remove_background("https://example.com/input.png", sync=True)

        assert isinstance(resp, RemoveBackgroundResult)
        assert resp.url == "https://example.com/output.png"
        assert resp.request_id is None
        assert resp.raw_json[STATUS_KEY] == "COMPLETED"


def test_remove_background_async_inprogress():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            REMOVE_BACKGROUND_ENDPOINT,
            json={
                STATUS_KEY: "IN_PROGRESS",
                REQUEST_ID_KEY: "req123",
                STATUS_URL_KEY: "https://engine.prod.bria-api.com/v2/status/req123",
            },
            status_code=200,
        )

        resp = client.rmbg.remove_background("https://example.com/input.png", sync=False)

        assert isinstance(resp, RemoveBackgroundResult)
        assert resp.url == "https://engine.prod.bria-api.com/v2/status/req123"
        assert resp.request_id == "req123"
        assert resp.raw_json[STATUS_KEY] == "IN_PROGRESS"


def test_remove_background_invalid_request():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            REMOVE_BACKGROUND_ENDPOINT,
            json={"error": {"message": "Invalid image format"}},
            status_code=400,
        )

        with pytest.raises(InvalidRequestError) as exc:
            client.rmbg.remove_background("bad_input.png")

        assert "Invalid image format" in str(exc.value)
