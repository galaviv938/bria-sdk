# bria/status.py

import requests
from typing import Dict, Any
from .constants import STATUS_ENDPOINT_TEMPLATE
from .utils import handle_response
from .exceptions import NotFoundError, BriaError

class StatusService:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("API token is required")
        self.api_token = api_token

    def get_status(self, request_id: str) -> Dict[str, Any]:
        """
        Fetch the status of an asynchronous Bria request by request_id.

        :param request_id: The ID returned by a previous async request.
        :return: JSON with status, possibly result.image_url or error details.
        :raises: NotFoundError if request_id is unknown, or other BriaError for other issues.
        """
        if not request_id:
            raise ValueError("request_id must be provided")

        url = STATUS_ENDPOINT_TEMPLATE.format(request_id=request_id)
        headers = {
            "api_token": self.api_token,
        }
        resp = requests.get(url, headers=headers)

        # If 404, map to NotFoundError
        if resp.status_code == 404:
            # Try to get JSON to show message
            try:
                err = resp.json()
                msg = err.get("error", {}).get("message", resp.text)
            except ValueError:
                msg = resp.text
            raise NotFoundError(f"Request ID {request_id} not found: {msg}")

        # If other than 200, handle generically
        if resp.status_code != 200:
            # Use handle_response but note handle_response may raise other error types
            return handle_response(resp)  # or you may want more specific mapping

        # status is 200 => check JSON
        data = resp.json()
        return data
