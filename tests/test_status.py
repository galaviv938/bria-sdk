import requests_mock
import pytest

from bria.client import Bria
from bria.exceptions import NotFoundError
from bria.constants import (
    STATUS_ENDPOINT_TEMPLATE,
    STATUS_KEY,
    RESULT_KEY,
    IMAGE_URL_KEY,
    REQUEST_ID_KEY,
    ERROR_KEY,
)
from bria.models import StatusSuccessResult, StatusErrorResult


def test_get_status_completed():
    client = Bria(api_token="fake_token")
    request_id = "req123"
    status_url = STATUS_ENDPOINT_TEMPLATE.format(request_id=request_id)

    with requests_mock.Mocker() as m:
        m.get(
            status_url,
            json={
                STATUS_KEY: "COMPLETED",
                REQUEST_ID_KEY: request_id,
                RESULT_KEY: {IMAGE_URL_KEY: "https://example.com/output.png"},
            },
            status_code=200,
        )

        resp = client.status.get_status(request_id)

        assert isinstance(resp, StatusSuccessResult)
        assert resp.status == "COMPLETED"
        assert resp.url == "https://example.com/output.png"
        assert resp.request_id == request_id
        assert resp.raw_json[STATUS_KEY] == "COMPLETED"


def test_get_status_error():
    client = Bria(api_token="fake_token")
    request_id = "req456"
    status_url = STATUS_ENDPOINT_TEMPLATE.format(request_id=request_id)

    with requests_mock.Mocker() as m:
        m.get(
            status_url,
            json={
                STATUS_KEY: ERROR_KEY,
                REQUEST_ID_KEY: request_id,
                ERROR_KEY: {"message": "Something went wrong"},
            },
            status_code=200,
        )

        resp = client.status.get_status(request_id)

        assert isinstance(resp, StatusErrorResult)
        assert resp.status == ERROR_KEY
        assert resp.request_id == request_id
        assert "message" in resp.error
        assert resp.error["message"] == "Something went wrong"


def test_get_status_not_found():
    client = Bria(api_token="fake_token")
    request_id = "unknown123"
    status_url = STATUS_ENDPOINT_TEMPLATE.format(request_id=request_id)

    with requests_mock.Mocker() as m:
        m.get(
            status_url,
            json={ERROR_KEY: {"message": "Not found"}},
            status_code=404,
        )

        with pytest.raises(NotFoundError) as excinfo:
            client.status.get_status(request_id)

        assert "not found" in str(excinfo.value).lower()
