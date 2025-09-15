import os
import time
import pytest
from bria.client import Bria

API_TOKEN = os.getenv("BRIA_API_TOKEN")
INPUT_IMAGE_URL = (
    "https://hips.hearstapps.com/hmg-prod/images/"
    "gettyimages-1279726757-651427fccdc51.jpg?crop=1.00xw:1.00xh;0,0&resize=1200:*"
)


@pytest.mark.e2e
@pytest.mark.skipif(API_TOKEN is None, reason="BRIA_API_TOKEN not set")
def test_remove_background_e2e_sync():
    client = Bria(api_token=API_TOKEN)

    result = client.edit.remove_background(image=INPUT_IMAGE_URL, sync=True)

    assert result.url, "Expected a valid output URL"
    assert result.request_id, "Expected a request_id"


@pytest.mark.e2e
@pytest.mark.skipif(API_TOKEN is None, reason="BRIA_API_TOKEN not set")
def test_remove_background_e2e_async():
    client = Bria(api_token=API_TOKEN)

    result = client.edit.remove_background(image=INPUT_IMAGE_URL, sync=False)
    assert result.request_id, "Expected a request_id"

    status = None
    for _ in range(20):
        status = client.status.get_status(result.request_id)
        if status.status == "COMPLETED":
            break
        time.sleep(1)

    assert status is not None
    assert status.status == "COMPLETED", f"Job failed with status: {status.status}"
    assert status.url, "Expected a valid output URL"