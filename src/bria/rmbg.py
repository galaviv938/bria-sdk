# bria/rmbg.py

import requests
from typing import Dict, Any
from src.bria.constants import (
    REMOVE_BACKGROUND_ENDPOINT,
    DEFAULT_PRESERVE_ALPHA,
    DEFAULT_SYNC,
    DEFAULT_INPUT_MODERATION,
    DEFAULT_OUTPUT_MODERATION, IMAGE_KEY, PRESERVE_ALPHA_KEY, SYNC_KEY, VISUAL_INPUT_MODERATION_KEY,
    VISUAL_OUTPUT_MODERATION_KEY, RESULT_KEY, IMAGE_URL_KEY, STATUS_KEY, REQUEST_ID_KEY, STATUS_URL_KEY,
)
from src.bria.models import RemoveBackgroundResult
from src.bria.utils import handle_response


class Rmbg:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("API token is required")
        self.api_token = api_token
        self.headers = {
            "api_token": self.api_token,
            "Content-Type": "application/json",
        }

    def remove_background(
            self,
            image: str,
            preserve_alpha: bool = DEFAULT_PRESERVE_ALPHA,
            sync: bool = DEFAULT_SYNC,
            visual_input_content_moderation: bool = DEFAULT_INPUT_MODERATION,
            visual_output_content_moderation: bool = DEFAULT_OUTPUT_MODERATION,
    ) -> RemoveBackgroundResult:
        """
        Remove the background of an image, via Bria's Remove Background API.
        """
        payload = self._build_payload(
            image,
            preserve_alpha,
            sync,
            visual_input_content_moderation,
            visual_output_content_moderation,
        )
        resp = self._send_request(payload)
        data = handle_response(resp)

        return self._build_result(data, sync)

    def _build_payload(
        self,
        image: str,
        preserve_alpha: bool,
        sync: bool,
        visual_input_content_moderation: bool,
        visual_output_content_moderation: bool,
    ) -> Dict[str, Any]:
        return {
            IMAGE_KEY: image,
            PRESERVE_ALPHA_KEY: preserve_alpha,
            SYNC_KEY: sync,
            VISUAL_INPUT_MODERATION_KEY: visual_input_content_moderation,
            VISUAL_OUTPUT_MODERATION_KEY: visual_output_content_moderation,
        }

    def _send_request(self, payload: Dict[str, Any]) -> requests.Response:
        return requests.post(REMOVE_BACKGROUND_ENDPOINT, headers=self.headers, json=payload)

    def _build_result(self, data: Dict[str, Any], is_sync: bool) -> RemoveBackgroundResult:
        if is_sync:
            return RemoveBackgroundResult(
                raw_json=data,
                url=data.get(RESULT_KEY, {}).get(IMAGE_URL_KEY),
                request_id=data.get(STATUS_KEY),
            )
        return RemoveBackgroundResult(
            raw_json=data,
            url=data.get(STATUS_URL_KEY),
            request_id=data.get(REQUEST_ID_KEY),
        )

