# tests/test_utils.py

import requests
import pytest

from bria.utils import handle_response
from bria.exceptions import AuthenticationError, InvalidRequestError


def test_handle_response_success(monkeypatch):
    class DummyResp:
        status_code = 200
        def json(self): return {"ok": True}

    resp = DummyResp()
    data = handle_response(resp)
    assert data["ok"] is True


def test_handle_response_invalid_request(monkeypatch):
    class DummyResp:
        status_code = 400
        def json(self): return {"error": {"message": "Bad request"}}

    resp = DummyResp()
    with pytest.raises(InvalidRequestError):
        handle_response(resp)


def test_handle_response_auth_error(monkeypatch):
    class DummyResp:
        status_code = 401
        def json(self): return {"error": {"message": "Unauthorized"}}

    resp = DummyResp()
    with pytest.raises(AuthenticationError):
        handle_response(resp)
