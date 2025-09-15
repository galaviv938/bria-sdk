import requests
from typing import Dict, Any, Union
import logging
from bria.image import Image
from src.bria.constants import (
    IMAGE_KEY,
    PRESERVE_ALPHA_KEY,
    SYNC_KEY,
    VISUAL_INPUT_MODERATION_KEY,
    VISUAL_OUTPUT_MODERATION_KEY,
    RESULT_KEY,
    IMAGE_URL_KEY,
    REQUEST_ID_KEY,
    STATUS_URL_KEY,
    EDIT,
    REMOVE_BACKGROUND,
)
from src.bria.models import EditSyncResult, EditAsyncResult
from src.bria.utils import handle_response

logger = logging.getLogger(__name__)


class Edit(Image):
    def __init__(self, api_token: str):
        super().__init__(api_token)
        self.edit_base_url = f"{self.image_base_url}/{EDIT}"

    def remove_background(
        self,
        image: str,
        preserve_alpha: bool = None,
        sync: bool = None,
        visual_input_content_moderation: bool = None,
        visual_output_content_moderation: bool = None,
    ) -> Union[EditSyncResult, EditAsyncResult]:
        logger.debug(f"Removing background image {image}")
        url = f"{self.edit_base_url}/{REMOVE_BACKGROUND}"
        payload = self._build_payload(
            image,
            preserve_alpha,
            sync,
            visual_input_content_moderation,
            visual_output_content_moderation,
        )
        resp = self._send_request(url, payload)
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
        logger.debug(f"Building payload for image {image}")
        field_map = {
            IMAGE_KEY: image,
            PRESERVE_ALPHA_KEY: preserve_alpha,
            SYNC_KEY: sync,
            VISUAL_INPUT_MODERATION_KEY: visual_input_content_moderation,
            VISUAL_OUTPUT_MODERATION_KEY: visual_output_content_moderation,
        }
        return {key: value for key, value in field_map.items() if value is not None}

    def _send_request(self, url: str, payload: Dict[str, Any]) -> requests.Response:
        logger.debug(f"Sending request to {url}")
        return requests.post(url, headers=self.headers, json=payload)

    def _build_result(
        self, data: Dict[str, Any], is_sync: bool
    ) -> Union[EditSyncResult, EditAsyncResult]:
        logger.debug(f"Building result: {data}")
        if is_sync:
            return EditSyncResult(
                url=data.get(RESULT_KEY, {}).get(IMAGE_URL_KEY),
                request_id=data.get(REQUEST_ID_KEY),
            )
        else:
            return EditAsyncResult(
                url=data.get(STATUS_URL_KEY),
                request_id=data.get(REQUEST_ID_KEY),
            )
