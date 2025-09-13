import os
import time

import pytest
from bria.client import Bria

API_TOKEN = os.getenv("BRIA_API_TOKEN")

@pytest.mark.skipif(API_TOKEN is None, reason="BRIA_API_TOKEN not set")
def test_remove_background_e2e_sync():
    client = Bria(api_token=API_TOKEN)
    input_image_url = "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1279726757-651427fccdc51.jpg?crop=1.00xw:1.00xh;0,0&resize=1200:*"

    result = client.rmbg.remove_background(image=input_image_url, sync=True)

    assert result.url is not None
    assert result.raw_json is not None
    assert "result" in result.raw_json

@pytest.mark.skipif(API_TOKEN is None, reason="BRIA_API_TOKEN not set")
def test_remove_background_e2e_async():
    client = Bria(api_token=API_TOKEN)
    input_image_url = "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1279726757-651427fccdc51.jpg?crop=1.00xw:1.00xh;0,0&resize=1200:*"
    result = client.rmbg.remove_background(image=input_image_url, sync=False)
    assert result.request_id is not None

    for _ in range(10):
        status = client.status.get_status(result.request_id)
        if status.status == "COMPLETED":
            break
        time.sleep(1)

    assert status.status == "COMPLETED"
    assert status.url is not None

