import pytest
from src.bria.utils import (
    parse_response_json,
    build_error_message,
    map_status_to_exception,
    handle_response,
)
from src.bria.exceptions import (
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    ServerError,
    BriaError,
    NotFoundError,
)


class DummyResponse:
    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        if self._json is None:
            raise ValueError("Invalid JSON")
        return self._json


def test_parse_response_json_valid():
    resp = DummyResponse(400, json_data={"error": {"message": "fail"}})
    assert parse_response_json(resp) == {"error": {"message": "fail"}}


def test_parse_response_json_invalid():
    resp = DummyResponse(400, json_data=None, text="Not JSON")
    assert parse_response_json(resp) == {"error": {"message": "Not JSON"}}


def test_build_error_message_with_all_fields():
    resp = DummyResponse(400)
    err_json = {"error": {"message": "fail", "code": "123"}, "request_id": "req_1"}
    msg = build_error_message(resp, err_json)
    assert "[400] fail" in msg
    assert "code 123" in msg
    assert "req_1" in msg


def test_build_error_message_minimal():
    resp = DummyResponse(400)
    err_json = {}
    msg = build_error_message(resp, err_json)
    assert "[400] Unknown error" in msg


@pytest.mark.parametrize(
    "status,exc",
    [
        (401, AuthenticationError),
        (403, AuthenticationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (400, InvalidRequestError),
        (415, InvalidRequestError),
        (422, InvalidRequestError),
        (460, InvalidRequestError),
        (500, ServerError),
        (502, ServerError),
        (999, BriaError),
    ],
)
def test_map_status_to_exception(status, exc):
    resp = DummyResponse(status)
    assert map_status_to_exception(resp) == exc


def test_handle_response_success():
    resp = DummyResponse(200, json_data={"ok": True})
    data = handle_response(resp)
    assert data == {"ok": True}


def test_handle_response_success_202():
    resp = DummyResponse(202, json_data={"ok": True})
    data = handle_response(resp)
    assert data == {"ok": True}


def test_handle_response_invalid_json_raises_briaerror():
    resp = DummyResponse(200, json_data=None, text="not json")
    with pytest.raises(BriaError):
        handle_response(resp)


@pytest.mark.parametrize(
    "status,exc",
    [
        (401, AuthenticationError),
        (403, AuthenticationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (400, InvalidRequestError),
        (415, InvalidRequestError),
        (422, InvalidRequestError),
        (460, InvalidRequestError),
        (500, ServerError),
        (502, ServerError),
        (999, BriaError),
    ],
)
def test_handle_response_raises(status, exc):
    resp = DummyResponse(
        status, json_data={"error": {"message": "fail"}, "request_id": "req_1"}
    )
    with pytest.raises(exc) as e:
        handle_response(resp)
    assert "fail" in str(e.value)
    assert "req_1" in str(e.value)
