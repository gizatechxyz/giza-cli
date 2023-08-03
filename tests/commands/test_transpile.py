import zipfile
from io import BytesIO
from unittest.mock import patch

from requests import HTTPError

from giza.client import ModelsClient
from giza.schemas.models import Model
from giza.utils.enums import ModelStatus
from tests.conftest import invoke_cli_runner


class ClientStub:
    def __init__(self, model, content) -> None:
        self.model = model
        self.content = content

    def get(self, *args, **kwargs):
        return self.model

    def create(self, *args, **kwargslf):
        return (self.model, "url")

    def _upload(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        return self.model

    def download(self, *args, **kwargs):
        return self.content


def test_transpilation_successful(tmpdir):
    def return_content():
        tmp = BytesIO()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr("file1.txt", "hi")
        return tmp.getvalue()

    model = Model(id=1, size=0, name="dummy", status=ModelStatus.COMPLETED)

    with patch(
        "giza.commands.transpile.ModelsClient",
        return_value=ClientStub(model, return_content()),
    ), patch("giza.commands.transpile.Path"), patch.object(
        ModelsClient, "get", return_value=model
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        ModelsClient, "_load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["transpile", "model", "--output-path", tmpdir, "--debug"]
        )

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

    model = Model(id=1, size=0, name="dummy", status=ModelStatus.COMPLETED)

    with patch(
        "giza.commands.transpile.ModelsClient",
        return_value=ClientStub(model, return_content()),
    ), patch("giza.commands.transpile.Path"), patch.object(
        ModelsClient, "get", return_value=model
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        ModelsClient, "_load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["transpile", "model", "--output-path", tmpdir], expected_error=True
        )

    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Something went wrong" in result.stdout
    assert "Error ->" in result.stdout
    assert result.exit_code == 1
