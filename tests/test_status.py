# tests/test_status.py

import requests_mock
import pytest

from bria.client import Bria
from bria.exceptions import NotFoundError
from bria.constants import STATUS_ENDPOINT_TEMPLATE


def test_get_status_completed():
    client = Bria(api_token="fake_token")
    request_id = "req123"
    status_url = STATUS_ENDPOINT_TEMPLATE.format(request_id=request_id)

    with requests_mock.Mocker() as m:
        m.get(
            status_url,
            json={
                "status": "COMPLETED",
                "result": {"image_url": "https://example.com/output.png"},
            },
            status_code=200,
        )

        resp = client.status.get_status(request_id)
        assert resp["status"] == "COMPLETED"
        assert "result" in resp
        assert resp["result"]["image_url"].endswith("output.png")


def test_get_status_not_found():
    client = Bria(api_token="fake_token")
    request_id = "unknown123"
    status_url = STATUS_ENDPOINT_TEMPLATE.format(request_id=request_id)

    with requests_mock.Mocker() as m:
        m.get(
            status_url,
            json={"error": {"message": "Not found"}},
            status_code=404,
        )

        with pytest.raises(NotFoundError) as excinfo:
            client.status.get_status(request_id)

        assert "not found" in str(excinfo.value).lower()
