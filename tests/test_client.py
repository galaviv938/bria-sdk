# tests/test_client.py

from bria.client import Bria
from bria.rmbg import Rmbg
from bria.status import StatusService


def test_client_initialization():
    client = Bria(api_token="fake_token")
    assert isinstance(client.rmbg, Rmbg)
    assert isinstance(client.status, StatusService)
