import requests_mock

from bria.client import Bria
from bria.constants import (
    ERROR_KEY,
    RESULT_KEY,
    IMAGE_URL_KEY,
    STATUS_KEY,
    REQUEST_ID_KEY,
)
from bria.models import StatusSuccessResult, StatusErrorResult


def test_get_status_completed():
    client = Bria(api_token="fake_token")
    request_id = "req123"
    status_url = f"{client.status.url}/{request_id}"

    response_json = {
        STATUS_KEY: "COMPLETED",
        RESULT_KEY: {IMAGE_URL_KEY: "https://example.com/output.png"},
        REQUEST_ID_KEY: request_id,
    }

    with requests_mock.Mocker() as m:
        m.get(status_url, json=response_json, status_code=200)
        result = client.status.get_status(request_id)

    # Assert type and fields
    assert isinstance(result, StatusSuccessResult)
    assert result.status == "COMPLETED"
    assert result.request_id == request_id
    assert result.url.endswith("output.png")


def test_get_status_in_progress():
    client = Bria(api_token="fake_token")
    request_id = "req456"
    status_url = f"{client.status.url}/{request_id}"

    response_json = {STATUS_KEY: "IN_PROGRESS", REQUEST_ID_KEY: request_id}

    with requests_mock.Mocker() as m:
        m.get(status_url, json=response_json, status_code=200)
        result = client.status.get_status(request_id)

    assert isinstance(result, StatusSuccessResult)
    assert result.status == "IN_PROGRESS"
    assert result.request_id == request_id
    assert result.url is None  # no URL yet


def test_get_status_error():
    client = Bria(api_token="fake_token")
    request_id = "req789"
    status_url = f"{client.status.url}/{request_id}"

    response_json = {
        STATUS_KEY: "ERROR",
        REQUEST_ID_KEY: request_id,
        ERROR_KEY: {"message": "Something went wrong"},
    }

    with requests_mock.Mocker() as m:
        m.get(status_url, json=response_json, status_code=200)
        result = client.status.get_status(request_id)

    assert isinstance(result, StatusErrorResult)
    assert result.status == "ERROR"
    assert result.request_id == request_id
    assert result.error["message"] == "Something went wrong"
