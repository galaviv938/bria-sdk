# bria/utils.py

import requests
from .exceptions import (
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    ServerError,
    BriaError,
)


def handle_response(response: requests.Response):
    """
    Handle API response and raise appropriate errors or return JSON.
    """

    if response.status_code in (200, 202):
        try:
            return response.json()
        except ValueError:
            raise BriaError(f"Invalid JSON response: {response.text}")

    try:
        err_json = response.json()
    except ValueError:
        err_json = {"error": {"message": response.text}}

    message = err_json.get("error", {}).get("message", "Unknown error")
    code = err_json.get("error", {}).get("code", "")
    request_id = err_json.get("request_id", "")

    err_msg = f"[{response.status_code}] {message}"
    if code:
        err_msg += f" (code {code})"
    if request_id:
        err_msg += f" | request_id: {request_id}"

    if response.status_code in (401, 403):
        raise AuthenticationError(err_msg)
    elif response.status_code == 429:
        raise RateLimitError(err_msg)
    elif response.status_code in (400, 404, 415, 422, 460):
        raise InvalidRequestError(err_msg)
    elif 500 <= response.status_code < 600:
        raise ServerError(err_msg)
    else:
        raise BriaError(err_msg)
