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
    key = "d261d7bfd3a44d808a6d7199dd5de436"
    b = Bria(key)
    imag = "https://static.nike.com/a/images/f_auto/dpr_1.0,cs_srgb/h_2432,c_limit/f24608dd-484a-47be-b27a-6e6c4e2ddf5d/back-to-school-le-migliori-scarpe-nike-per-il-rientro-a-scuola.jpg"
    res = b.rmbg.remove_background(image=imag,sync=False)
    b.status.get_status(res.request_id)
    x=1
