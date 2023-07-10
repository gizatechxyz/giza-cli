import zipfile
from io import BytesIO
from unittest.mock import patch

from requests import HTTPError

from giza.client import TranspileClient
from tests.conftest import invoke_cli_runner


def test_transpilation_successful(tmpdir):
    class StubResponse:
        tmp = BytesIO()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr("file1.txt", "hi")
        content = tmp.getvalue()

    with patch.object(
        TranspileClient, "transpile", return_value=StubResponse()
    ) as mock_transpile, patch("builtins.open") as mock_open:
        result = invoke_cli_runner(["transpile", "model", "--output-path", tmpdir])

    mock_transpile.assert_called_once()
    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Reading model from path" in result.stdout
    assert "Transpilation recieved" in result.stdout
    assert result.exit_code == 0


def test_transpilation_http_error(tmpdir):
    with patch.object(TranspileClient, "transpile", side_effect=HTTPError), patch(
        "builtins.open"
    ) as mock_open, patch("giza.commands.transpile.get_response_info", return_value={}):
        result = invoke_cli_runner(
            ["transpile", "model", "--output-path", tmpdir], expected_error=True
        )

    mock_open.assert_called_once_with("model", "rb")
    assert "Error at transpilation" in result.stdout
    assert result.exit_code == 1


def test_transpilation_bad_zip(tmpdir):
    class StubResponse:
        content = b"some bytes"

    with patch.object(
        TranspileClient, "transpile", return_value=StubResponse()
    ) as mock_transpile, patch("builtins.open") as mock_open:
        result = invoke_cli_runner(
            ["transpile", "model", "--output-path", tmpdir], expected_error=True
        )

    mock_transpile.assert_called_once()
    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Something went wrong" in result.stdout
    assert "Error ->" in result.stdout
    assert result.exit_code == 1
