# bria/rmbg.py

import requests
from typing import Dict, Any
from .constants import (
    REMOVE_BACKGROUND_ENDPOINT,
    DEFAULT_PRESERVE_ALPHA,
    DEFAULT_SYNC,
    DEFAULT_INPUT_MODERATION,
    DEFAULT_OUTPUT_MODERATION,
)
from .utils import handle_response


class Rmbg:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("API token is required")
        self.api_token = api_token

    def remove_background(
        self,
        image: str,
        preserve_alpha: bool = DEFAULT_PRESERVE_ALPHA,
        sync: bool = DEFAULT_SYNC,
        visual_input_content_moderation: bool = DEFAULT_INPUT_MODERATION,
        visual_output_content_moderation: bool = DEFAULT_OUTPUT_MODERATION,
    ) -> Dict[str, Any]:
        """
        Remove the background of an image, via Bria's Remove Background API.
        """

        headers = {
            "api_token": self.api_token,
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "image": image,
            "preserve_alpha": preserve_alpha,
            "sync": sync,
            "visual_input_content_moderation": visual_input_content_moderation,
            "visual_output_content_moderation": visual_output_content_moderation,
        }

        resp = requests.post(REMOVE_BACKGROUND_ENDPOINT, headers=headers, json=payload)
        return handle_response(resp)
