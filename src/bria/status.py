import requests
from typing import Dict, Any

from bria.models import StatusResult, StatusErrorResult, StatusSuccessResult
from src.bria.constants import STATUS_ENDPOINT_TEMPLATE, RESULT_KEY, IMAGE_URL_KEY, STATUS_KEY, REQUEST_ID_KEY, \
    ERROR_KEY, SEED_KEY, PROMPT_KEY, REFINED_PROMPT_KEY
from src.bria.utils import handle_response

class StatusService:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("API token is required")
        self.api_token = api_token
        self.headers = {"api_token": self.api_token}

    def get_status(self, request_id: str) -> StatusResult:
        """
        Fetch the status of an asynchronous Bria request by request_id.

        :param request_id: The ID returned by a previous async request.
        :return: JSON with status, possibly result.image_url or error details.
        :raises: NotFoundError if request_id is unknown, or other BriaError for other issues.
        """
        if not request_id:
            raise ValueError("request_id must be provided")

        url = STATUS_ENDPOINT_TEMPLATE.format(request_id=request_id)
        resp = requests.get(url, headers=self.headers)

        data = handle_response(resp)
        return self._build_result(data)

    def _build_result(self, data: Dict[str, Any]) -> StatusResult:
        field_map = {
            "status": lambda d: d.get(STATUS_KEY),
            "request_id": lambda d: d.get(REQUEST_ID_KEY),
        }
        status_class = StatusSuccessResult
        if data.get(STATUS_KEY) == ERROR_KEY:
            status_class = StatusErrorResult
            field_map[ERROR_KEY] = lambda d: d.get(ERROR_KEY)
        else:
            field_map.update({
                "url": lambda d: d.get(RESULT_KEY, {}).get(IMAGE_URL_KEY),
                "seed": lambda d: d.get(SEED_KEY),
                "prompt": lambda d: d.get(PROMPT_KEY),
                "refined_prompt": lambda d: d.get(REFINED_PROMPT_KEY),
            })
        filtered_fields = {key: func(data) for key, func in field_map.items() if func(data) is not None}
        filtered_fields["raw_json"] = data
        return status_class(**filtered_fields)