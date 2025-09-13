import os

from src.bria.rmbg import Rmbg
from src.bria.status import StatusService

class Bria:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("api_token must be provided")
        self.api_token = api_token
        self.rmbg = Rmbg(api_token)
        self.status = StatusService(api_token)



if __name__ == '__main__':
    key = os.getenv("BRIA_API_TOKEN")
    b = Bria(key)
    imag = "ps://hips.hearstapps.com/hmg-prod/images/neon-colored-epipremnum-aureum-lemon-lime-royalty-free-image-1724090039.jpg?crop=0.910xw:0.911xh;0.0680xw,0.0332xh&resize=1200:*"
    res = b.rmbg.remove_background(image=imag,sync=False)
    b.status.get_status(res.request_id)
    x=1
