from src.bria.client import Bria
from src.bria.edit import Edit
from src.bria.status import StatusService


def test_client_initialization():
    client = Bria(api_token="fake_token")
    assert isinstance(client.rmbg, Edit)
    assert isinstance(client.status, StatusService)
