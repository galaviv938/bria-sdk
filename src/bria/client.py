from src.bria.edit import Edit
from src.bria.status import StatusService


class Bria:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("api_token must be provided")
        self.api_token = api_token
        self.edit = Edit(api_token)
        self.status = StatusService(api_token)

if __name__ == '__main__':
    import os
    API_TOKEN = os.getenv("BRIA_API_TOKEN")

    b = Bria('d3fc93bca79948d2ac1c01e046e35753')
    input_image_url = "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1279726757-651427fccdc51.jpg?crop=1.00xw:1.00xh;0,0&resize=1200:*"
    x = b.edit.remove_background(input_image_url)
    y= 0