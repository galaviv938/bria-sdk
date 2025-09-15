from bria.constants import BASE_URL


class Image:
    def __init__(self, api_token: str):
        self.image_base_url = f"{BASE_URL}/image"
        self.api_token = api_token
        self.headers = {
            "api_token": self.api_token,
            "Content-Type": "application/json",
        }
