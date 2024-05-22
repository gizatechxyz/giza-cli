import os
from unittest.mock import patch

import pytest

from giza.cli.client import GIZA_TOKEN_VARIABLE, ApiClient
from giza.cli.utils.decorators import auth


def get_client():
    class DummyClient(ApiClient):
        @auth
        def foo(self, *args, **kwargs):
            return True

    return DummyClient("http://dummy_host")


def test_auth_from_env_ok():
    api_client = get_client()

    with patch.dict(os.environ, {GIZA_TOKEN_VARIABLE: "mytoken"}), patch.object(
        ApiClient, "_is_expired", return_value=False
    ) as mock_expired:
        result = api_client.foo()

    mock_expired.assert_called()
    assert result is True


def test_auth_expired():
    api_client = get_client()

    with patch.dict(os.environ, {GIZA_TOKEN_VARIABLE: "mytoken"}), patch.object(
        ApiClient, "_is_expired", return_value=True
    ) as mock_expired, pytest.raises(Exception):
        _ = api_client.foo()

    mock_expired.assert_called()


def test_auth_no_token():
    api_client = get_client()

    with patch.dict(os.environ, {GIZA_TOKEN_VARIABLE: "mytoken"}), patch.object(
        ApiClient,
        "retrieve_token",
    ) as mock_retireved, pytest.raises(Exception):
        _ = api_client.foo()

    mock_retireved.assert_called()
