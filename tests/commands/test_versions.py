import zipfile
from io import BytesIO
from unittest.mock import patch

from pydantic import ValidationError
from pydantic_core import InitErrorDetails
from requests.exceptions import HTTPError

from giza.cli.commands.versions import VersionsClient, VersionStatus
from giza.cli.schemas.models import Model, ModelList
from giza.cli.schemas.versions import Version, VersionList
from giza.cli.utils.enums import Framework
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


# Test successful version retrieval
def test_versions_get():
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )
    with patch.object(VersionsClient, "get", return_value=version) as mock_get:
        result = invoke_cli_runner(
            ["versions", "get", "--model-id", "1", "--version-id", "1"]
        )

    assert result.exit_code == 0
    mock_get.assert_called_once()
    assert "Retrieving version information" in result.stdout


# Test version retrieval that throws an HTTPError
def test_versions_get_http_error():
    with patch.object(VersionsClient, "get", side_effect=HTTPError), patch(
        "giza.cli.utils.exception_handling.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            ["versions", "get", "--model-id", "1", "--version-id", "1"],
            expected_error=True,
        )

    assert result.exit_code == 1
    assert "Could not perform the action on the resource" in result.stdout


# Test version retrieval with invalid version id
def test_versions_get_invalid_id():
    with patch.object(
        VersionsClient,
        "get",
        side_effect=ValidationError.from_exception_data(
            line_errors=[InitErrorDetails(type="missing")],
            title="Resource validation error",
        ),
    ), patch("giza.cli.utils.exception_handling.get_response_info", return_value={}):
        result = invoke_cli_runner(
            ["versions", "get", "--model-id", "1", "--version-id", "1"],
            expected_error=True,
        )

    assert result.exit_code == 1
    assert "Resource validation error" in result.stdout


# Test successful version listing
def test_versions_list():
    versions = VersionList(
        root=[
            Version(
                version=1,
                size=1,
                description="test_version",
                status=VersionStatus.COMPLETED,
                created_date="2021-08-31T15:00:00.000000",
                last_update="2021-08-31T15:00:00.000000",
                framework=Framework.CAIRO,
            )
        ]
    )
    with patch.object(VersionsClient, "list", return_value=versions) as mock_list:
        result = invoke_cli_runner(["versions", "list", "--model-id", "1"])

    assert result.exit_code == 0
    mock_list.assert_called_once()
    assert "Listing versions for the model" in result.stdout


# Test version listing with server error
def test_versions_list_server_error():
    with patch.object(VersionsClient, "list", side_effect=HTTPError), patch(
        "giza.cli.utils.exception_handling.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            ["versions", "list", "--model-id", "1"], expected_error=True
        )

    assert result.exit_code == 1
    assert "Could not perform the action on the resource" in result.stdout


# Test successful version transpilation
def test_versions_transpile_successful(tmpdir):
    def return_content():
        tmp = BytesIO()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr("file1.txt", "hi")
        return {"model": tmp.getvalue()}

    models = ModelList(
        root=[
            Model(
                id=1,
                name="test_model",
                description="test_description",
                created_at="2021-08-31T15:00:00.000000",
                updated_at="2021-08-31T15:00:00.000000",
            )
        ]
    )

    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )

    with patch(
        "giza.cli.frameworks.cairo.VersionsClient",
        return_value=ClientStub(version, return_content()),
    ), patch(
        "giza.cli.frameworks.cairo.ModelsClient.list",
        return_value=models,
    ), patch(
        "giza.cli.frameworks.cairo.Path"
    ), patch.object(
        VersionsClient, "get", return_value=version
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        VersionsClient, "_load_credentials_file"
    ), patch(
        "giza.cli.frameworks.cairo.ModelsClient._load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["versions", "transpile", "model", "--output-path", tmpdir, "--debug"]
        )

    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Reading model from path" in result.stdout
    assert "Downloading model" in result.stdout
    assert "model saved at" in result.stdout
    assert result.exit_code == 0


# Test version transpilation with HTTP error
def test_versions_transpile_http_error(tmpdir):
    with patch(
        "giza.cli.frameworks.cairo.ModelsClient.get_by_name", side_effect=HTTPError
    ), patch(
        "giza.cli.utils.exception_handling.get_response_info", return_value={}
    ), patch(
        "giza.cli.frameworks.cairo.Path"
    ), patch.object(
        VersionsClient, "_load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["versions", "transpile", "model", "--output-path", tmpdir],
            expected_error=True,
        )

    assert "Error at transpilation" in result.stdout
    assert result.exit_code == 1


# Test version transpilation with file
def test_versions_transpile_file(tmpdir):
    def return_content():
        return {"model": b"some bytes"}

    models = ModelList(
        root=[
            Model(
                id=1,
                name="test_model",
                description="test_description",
                created_at="2021-08-31T15:00:00.000000",
                updated_at="2021-08-31T15:00:00.000000",
            )
        ]
    )

    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )

    with patch(
        "giza.cli.frameworks.cairo.VersionsClient",
        return_value=ClientStub(version, return_content()),
    ), patch(
        "giza.cli.frameworks.cairo.ModelsClient.list",
        return_value=models,
    ), patch(
        "giza.cli.frameworks.cairo.Path"
    ), patch.object(
        VersionsClient, "get", return_value=version
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        VersionsClient, "_load_credentials_file"
    ), patch(
        "giza.cli.frameworks.cairo.ModelsClient._load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["versions", "transpile", "model", "--output-path", tmpdir],
            expected_error=True,
        )

    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Transpilation is fully compatible" in result.stdout
    assert "Downloading model" in result.stdout
    assert result.exit_code == 0


# Test successful version download
def test_versions_download_successful(tmpdir):
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )

    def return_content():
        tmp = BytesIO()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr("file1.txt", "hi")
        return {"model": tmp.getvalue()}

    with patch.object(VersionsClient, "get", return_value=version), patch.object(
        VersionsClient, "download", return_value=return_content()
    ), patch("builtins.open") as mock_open, patch(
        "giza.cli.client.VersionsClient._load_credentials_file"
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "download",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--output-path",
                tmpdir,
            ]
        )

    mock_open.assert_called()
    assert "Data is ready, downloading!" in result.stdout
    assert result.exit_code == 0


# Test version download with server error
def test_versions_download_server_error():
    with patch.object(VersionsClient, "get", side_effect=HTTPError), patch(
        "giza.cli.utils.exception_handling.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "download",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--output-path",
                "path",
            ],
            expected_error=True,
        )

    assert result.exit_code == 1
    assert "Could not perform the action on the resource" in result.stdout


# Test version download but a file, imitating a sierra file
def test_versions_download_file(tmpdir):
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )

    def return_content():
        return {"model": b"some bytes"}

    with patch.object(VersionsClient, "get", return_value=version), patch.object(
        VersionsClient, "download", return_value=return_content()
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "download",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--output-path",
                tmpdir,
            ],
            expected_error=True,
        )

    assert "saved at" in result.stdout
    assert result.exit_code == 0


# Test version download with missing model_id and version_id
def test_versions_download_missing_ids():
    with patch.object(VersionsClient, "get", side_effect=HTTPError), patch(
        "giza.cli.utils.exception_handling.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "download",
                "--output-path",
                "path",
            ],
            expected_error=True,
        )

    assert "Model ID and version ID are required" in result.stdout
    assert result.exit_code == 1


def test_versions_update_successful():
    version = Version(
        version=1,
        size=1,
        description="updated_description",
        status=VersionStatus.PARTIALLY_SUPPORTED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )
    updated_version = version.model_copy()
    updated_version.status = VersionStatus.COMPLETED

    with patch.object(VersionsClient, "get", return_value=version), patch.object(
        VersionsClient, "upload_cairo", return_value=updated_version
    ), patch("giza.cli.commands.versions.scarb_build"), patch(
        "giza.cli.commands.versions.zip_folder"
    ), patch(
        "giza.cli.commands.versions.update_sierra"
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "update",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--model-path",
                "path",
            ]
        )

    assert "Checking version" in result.stdout
    assert result.exit_code == 0
    assert "Version updated" in result.stdout


def test_versions_update_server_error():
    version = Version(
        version=1,
        size=1,
        description="updated_description",
        status=VersionStatus.PARTIALLY_SUPPORTED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )
    with patch.object(
        VersionsClient, "upload_cairo", side_effect=HTTPError
    ), patch.object(VersionsClient, "get", return_value=version), patch(
        "giza.cli.utils.exception_handling.get_response_info", return_value={}
    ), patch(
        "giza.cli.commands.versions.scarb_build"
    ), patch(
        "giza.cli.commands.versions.zip_folder"
    ), patch(
        "giza.cli.commands.versions.update_sierra",
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "update",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--model-path",
                "path",
            ],
            expected_error=True,
        )

    assert "Could not perform the action on the resource" in result.stdout
    assert result.exit_code == 1


def test_versions_update_missing_ids():
    with patch.object(VersionsClient, "update", side_effect=HTTPError), patch(
        "giza.cli.utils.exception_handling.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "update",
            ],
            expected_error=True,
        )

    assert "Model ID and version ID are required to update the version" in result.stdout
    assert result.exit_code == 1
