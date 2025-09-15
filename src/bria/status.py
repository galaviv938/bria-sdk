import requests
from typing import Dict, Any
import logging
from bria.models import StatusResult, StatusErrorResult, StatusSuccessResult
from src.bria.constants import (
    RESULT_KEY,
    IMAGE_URL_KEY,
    STATUS_KEY,
    REQUEST_ID_KEY,
    ERROR_KEY,
    SEED_KEY,
    PROMPT_KEY,
    REFINED_PROMPT_KEY,
    BASE_URL,
)
from src.bria.utils import handle_response

logger = logging.getLogger(__name__)


class StatusService:
    def __init__(self, api_token: str):
        self.url = f"{BASE_URL}/status"
        self.api_token = api_token
        self.headers = {"api_token": self.api_token}

    def get_status(self, request_id: str) -> StatusResult:
        logger.debug(f"Getting status for request_id: {request_id}")
        if not request_id:
            raise ValueError("request_id must be provided")

        url = f"{self.url}/{request_id}"
        resp = self._send_request(url)
        data = handle_response(resp)
        return self._build_result(data)

    def _send_request(self, url: str) -> requests.Response:
        logger.debug(f"Sending request to url: {url}")
        return requests.get(url, headers=self.headers)

    def _build_result(self, data: Dict[str, Any]) -> StatusResult:
        logger.debug(f"Building result from data: {data}")
        field_map = {
            "status": data.get(STATUS_KEY),
            "request_id": data.get(REQUEST_ID_KEY),
        }
        status_class = StatusSuccessResult
        if data.get(STATUS_KEY).lower() == ERROR_KEY:
            status_class = StatusErrorResult
            field_map[ERROR_KEY] = data.get(ERROR_KEY)
        else:
            field_map.update(
                {
                    "url": data.get(RESULT_KEY, {}).get(IMAGE_URL_KEY),
                    "seed": data.get(SEED_KEY),
                    "prompt": data.get(PROMPT_KEY),
                    "refined_prompt": data.get(REFINED_PROMPT_KEY),
                }
            )
        filtered_fields = {
            key: value for key, value in field_map.items() if value is not None
        }
        return status_class(**filtered_fields)
