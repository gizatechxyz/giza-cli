import json
from unittest.mock import MagicMock, patch

import pytest
from jose import ExpiredSignatureError
from requests import HTTPError

from giza.client import DEFAULT_API_VERSION, ApiClient


class ResponseStub:
    def __init__(self, data, status_code, exception=None) -> None:
        self.status_code = status_code
        self.data = data
        self.exception = exception

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.exception is not None:
            raise self.exception

    def text(self):
        return self.data


def test_api_client_init_no_credentials(tmpdir):
    with patch("pathlib.Path.home", return_value=tmpdir):
        client = ApiClient("http://dummy_host")

    assert client.url == f"http://dummy_host/api/{DEFAULT_API_VERSION}"
    assert client.default_headers == {}
    assert client._default_credentials == {}


def test_api_client_init_with_credentials(tmpdir):
    credentials = {"token": "gizatoken"}
    giza_folder = tmpdir / ".giza"
    giza_folder.mkdir()
    with open(giza_folder / ".credentials.json", "w") as f:
        json.dump(credentials, f)

    with patch("pathlib.Path.home", return_value=tmpdir):
        client = ApiClient("http://dummy_host")

    assert client.url == f"http://dummy_host/api/{DEFAULT_API_VERSION}"
    assert client.default_headers == {}
    assert client._default_credentials == credentials


def test_api_client__get_oauth_ok(tmpdir):
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.post",
        return_value=ResponseStub(
            {"access_token": "token", "token_type": "bearer"}, 200
        ),
    ):
        client = ApiClient("http://dummy_host")
        client._get_oauth("user", "password")

    assert client.token == "token"


def test_api_client__get_oauth_http_error(tmpdir):
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.post", return_value=ResponseStub({""}, 400, HTTPError())
    ), pytest.raises(HTTPError):
        client = ApiClient("http://dummy_host")
        client._get_oauth("user", "password")


def test_api_client__get_oauth_decode_error(tmpdir, capsys):
    mock = MagicMock()
    mock.json.side_effect = json.JSONDecodeError("", "", 1)
    mock.text = "Response text"
    mock.status_code = 500
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.post", return_value=mock
    ) as mock_post, pytest.raises(json.JSONDecodeError):
        client = ApiClient("http://dummy_host")
        client._get_oauth("user", "password")
    mock_post.assert_called_once()
    captured = capsys.readouterr()

    assert "Response text" in captured.out
    assert "Status Code -> 500" in captured.out


def test_api_client__write_credentials(tmpdir):
    giza_dir = tmpdir / ".giza"
    with patch("pathlib.Path.home", return_value=tmpdir):
        client = ApiClient("http://dummy_host", token="token")
        client._write_credentials()

    assert giza_dir.exists()
    assert (giza_dir / ".credentials.json").exists()


def test_api_client__is_expired_false(tmpdir):
    with patch("pathlib.Path.home", return_value=tmpdir), patch("jose.jwt.decode"):
        client = ApiClient("http://dummy_host")
        expired = client._is_expired(token="token")

    assert not expired


def test_api_client__is_expired_true(tmpdir):
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "jose.jwt.decode", side_effect=ExpiredSignatureError
    ):
        client = ApiClient("http://dummy_host")
        expired = client._is_expired(token="token")

    assert expired
