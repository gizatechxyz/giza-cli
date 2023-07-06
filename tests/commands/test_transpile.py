import zipfile
from io import BytesIO
from unittest.mock import patch

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
