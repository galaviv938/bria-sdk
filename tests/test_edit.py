import requests_mock
import pytest

from bria.models import EditSyncResult, EditAsyncResult
from src.bria.client import Bria
from src.bria.constants import (
    RESULT_KEY,
    IMAGE_URL_KEY,
    STATUS_KEY,
    REQUEST_ID_KEY,
    STATUS_URL_KEY, REMOVE_BACKGROUND,
)
from src.bria.exceptions import InvalidRequestError


def test_remove_background_sync_success():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            url= f"{client.edit.image_base_url}/{REMOVE_BACKGROUND}",
            json={
                STATUS_KEY: "COMPLETED",
                RESULT_KEY: {IMAGE_URL_KEY: "https://example.com/output.png"},
            },
            status_code=200,
        )

        resp = client.edit.remove_background("https://example.com/input.png", sync=True)

        assert isinstance(resp, EditAsyncResult)
        assert resp.url == "https://example.com/output.png"
        assert resp.request_id is None

def test_remove_background_async_inprogress():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            url= f"{client.edit.image_base_url}/{REMOVE_BACKGROUND}",
            json={
                STATUS_KEY: "IN_PROGRESS",
                REQUEST_ID_KEY: "req123",
                STATUS_URL_KEY: "https://engine.prod.bria-api.com/v2/status/req123",
            },
            status_code=200,
        )

        resp = client.edit.remove_background(
            "https://example.com/input.png", sync=False
        )

        assert isinstance(resp, EditAsyncResult)
        assert resp.url == "https://engine.prod.bria-api.com/v2/status/req123"
        assert resp.request_id == "req123"


def test_remove_background_invalid_request():
    client = Bria(api_token="fake_token")

    with requests_mock.Mocker() as m:
        m.post(
            url= f"{client.edit.image_base_url}/{REMOVE_BACKGROUND}",
            json={"error": {"message": "Invalid image format"}},
            status_code=400,
        )

        with pytest.raises(InvalidRequestError) as exc:
            client.edit.remove_background("bad_input.png")

        assert "Invalid image format" in str(exc.value)
