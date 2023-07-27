import zipfile
from io import BytesIO
from unittest.mock import patch

from requests import HTTPError

from giza.client import ModelsClient, TranspileClient
from giza.schemas.models import Model
from giza.utils.enums import ModelStatus
from tests.conftest import invoke_cli_runner


def test_transpilation_successful(tmpdir):
    def return_content():
        tmp = BytesIO()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr("file1.txt", "hi")
        return tmp.getvalue()

    model = Model(id=1, size=0, name="dummy", user_id=1, status=ModelStatus.COMPLETED)

    with patch.object(
        ModelsClient, "create", return_value=(model, "url")
    ) as mock_transpile, patch.object(
        ModelsClient,
        "_upload",
    ), patch.object(
        ModelsClient,
        "update",
    ), patch.object(
        ModelsClient, "download", return_value=return_content()
    ), patch(
        "giza.commands.transpile.Path"
    ), patch.object(
        ModelsClient, "get", return_value=model
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        ModelsClient, "_load_credentials_file"
    ):
        result = invoke_cli_runner(["transpile", "model", "--output-path", tmpdir])

    mock_transpile.assert_called_once()
    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Reading model from path" in result.stdout
    assert "Transpilation recieved" in result.stdout
    assert result.exit_code == 0


def test_transpilation_http_error(tmpdir):
    with patch.object(ModelsClient, "create", side_effect=HTTPError), patch(
        "giza.commands.transpile.get_response_info", return_value={}
    ), patch("giza.commands.transpile.Path"), patch.object(
        ModelsClient, "_load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["transpile", "model", "--output-path", tmpdir], expected_error=True
        )

    assert "Error at transpilation" in result.stdout
    assert result.exit_code == 1


def test_transpilation_bad_zip(tmpdir):
    def return_content():
        return b"some bytes"

    model = Model(id=1, size=0, name="dummy", user_id=1, status=ModelStatus.COMPLETED)

    with patch.object(
        ModelsClient, "create", return_value=(model, "url")
    ) as mock_transpile, patch.object(
        ModelsClient,
        "_upload",
    ), patch.object(
        ModelsClient,
        "update",
    ), patch.object(
        ModelsClient, "download", return_value=return_content()
    ), patch(
        "giza.commands.transpile.Path"
    ), patch.object(
        ModelsClient, "get", return_value=model
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        ModelsClient, "_load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["transpile", "model", "--output-path", tmpdir], expected_error=True
        )

    mock_transpile.assert_called_once()
    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Something went wrong" in result.stdout
    assert "Error ->" in result.stdout
    assert result.exit_code == 1
