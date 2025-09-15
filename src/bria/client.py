from src.bria.edit import Edit
from src.bria.status import StatusService


class Bria:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("api_token must be provided")
        self.api_token = api_token
        self.edit = Edit(api_token)
        self.status = StatusService(api_token)
