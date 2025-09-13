# bria/client.py

from .rmbg import Rmbg
from .status import StatusService

class Bria:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("api_token must be provided")
        self.api_token = api_token
        self.rmbg = Rmbg(api_token)
        self.status = StatusService(api_token)



if __name__ == '__main__':
    key = "d261d7bfd3a44d808a6d7199dd5de436"
    b = Bria(key)
