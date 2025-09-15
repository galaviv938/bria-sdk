import requests
from src.bria.exceptions import (
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    ServerError,
    BriaError,
    NotFoundError,
)

STATUS_EXCEPTIONS = {
    400: InvalidRequestError,
    401: AuthenticationError,
    403: AuthenticationError,
    404: NotFoundError,
    415: InvalidRequestError,
    422: InvalidRequestError,
    429: RateLimitError,
    460: InvalidRequestError,
}


def parse_response_json(response: requests.Response):
    try:
        return response.json()
    except ValueError:
        return {"error": {"message": response.text}}


def build_error_message(response: requests.Response, err_json: dict) -> str:
    error_info = err_json.get("error", {})
    message = error_info.get("message", "Unknown error")
    code = error_info.get("code", "")
    request_id = err_json.get("request_id", "")

    err_msg = f"[{response.status_code}] {message}"
    if code:
        err_msg += f" (code {code})"
    if request_id:
        err_msg += f" | request_id: {request_id}"
    return err_msg


def map_status_to_exception(response: requests.Response) -> type[Exception]:
    if 500 <= response.status_code < 600:
        return ServerError
    return STATUS_EXCEPTIONS.get(response.status_code, BriaError)


def handle_response(response: requests.Response):
    if response.status_code in (200, 202):
        try:
            return response.json()
        except ValueError:
            raise BriaError(f"Invalid JSON response: {response.text}")

    err_json = parse_response_json(response)
    err_msg = build_error_message(response, err_json)
    exc_class = map_status_to_exception(response)

    raise exc_class(err_msg)