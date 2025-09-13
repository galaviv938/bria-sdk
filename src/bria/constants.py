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

# Payload keys
IMAGE_KEY = "image"
PRESERVE_ALPHA_KEY = "preserve_alpha"
SYNC_KEY = "sync"
VISUAL_INPUT_MODERATION_KEY = "visual_input_content_moderation"
VISUAL_OUTPUT_MODERATION_KEY = "visual_output_content_moderation"

# Response keys
RESULT_KEY = "result"
IMAGE_URL_KEY = "image_url"
STATUS_KEY = "status"
STATUS_URL_KEY = "status_url"
REQUEST_ID_KEY = "request_id"
ERROR_KEY = "error"
SEED_KEY = "seed"
PROMPT_KEY = "prompt"
REFINED_PROMPT_KEY = "refined_prompt"