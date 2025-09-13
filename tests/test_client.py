# tests/test_client.py

from src.bria.client import Bria
from src.bria.rmbg import Rmbg
from src.bria.status import StatusService


def test_client_initialization():
    client = Bria(api_token="fake_token")
    assert isinstance(client.rmbg, Rmbg)
    assert isinstance(client.status, StatusService)
