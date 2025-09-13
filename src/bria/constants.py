# bria/constants.py

# Base API URL
BASE_URL = "https://engine.prod.bria-api.com/v2"

# Endpoints
REMOVE_BACKGROUND_ENDPOINT = f"{BASE_URL}/image/edit/remove_background"
STATUS_ENDPOINT_TEMPLATE = f"{BASE_URL}/status/{{request_id}}"

# Default values
DEFAULT_PRESERVE_ALPHA = True
DEFAULT_SYNC = False
DEFAULT_INPUT_MODERATION = False
DEFAULT_OUTPUT_MODERATION = False
