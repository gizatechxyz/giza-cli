import zipfile
from io import BytesIO
from unittest.mock import patch

from pydantic.error_wrappers import ValidationError
from requests.exceptions import HTTPError

from giza.commands.versions import VersionsClient, VersionStatus
from giza.schemas.models import Model, ModelList
from giza.schemas.versions import Version, VersionList
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
        "giza.commands.versions.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            ["versions", "get", "--model-id", "1", "--version-id", "1"],
            expected_error=True,
        )

    assert result.exit_code == 1
    assert "Could not retrieve version information" in result.stdout


# Test version retrieval with invalid version id
def test_versions_get_invalid_id():
    with patch.object(
        VersionsClient, "get", side_effect=ValidationError(errors=[], model=Version)
    ), patch("giza.commands.versions.get_response_info", return_value={}):
        result = invoke_cli_runner(
            ["versions", "get", "--model-id", "1", "--version-id", "1"],
            expected_error=True,
        )

    assert result.exit_code == 1
    assert "Version validation error" in result.stdout


# Test successful version listing
def test_versions_list():
    versions = VersionList(
        __root__=[
            Version(
                version=1,
                size=1,
                description="test_version",
                status=VersionStatus.COMPLETED,
                created_date="2021-08-31T15:00:00.000000",
                last_update="2021-08-31T15:00:00.000000",
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
        "giza.commands.versions.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            ["versions", "list", "--model-id", "1"], expected_error=True
        )

    assert result.exit_code == 1
    assert "Could not list versions for the model" in result.stdout


# Test successful version transpilation
def test_versions_transpile_successful(tmpdir):
    def return_content():
        tmp = BytesIO()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr("file1.txt", "hi")
        return tmp.getvalue()

    models = ModelList(
        __root__=[
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
    )

    with patch(
        "giza.commands.versions.VersionsClient",
        return_value=ClientStub(version, return_content()),
    ), patch(
        "giza.commands.versions.ModelsClient.list",
        return_value=models,
    ), patch(
        "giza.commands.versions.Path"
    ), patch.object(
        VersionsClient, "get", return_value=version
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        VersionsClient, "_load_credentials_file"
    ), patch(
        "giza.commands.versions.ModelsClient._load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["versions", "transpile", "model", "--output-path", tmpdir, "--debug"]
        )

    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Reading model from path" in result.stdout
    assert "Transpilation recieved" in result.stdout
    assert result.exit_code == 0


# Test version transpilation with HTTP error
def test_versions_transpile_http_error(tmpdir):
    with patch(
        "giza.commands.versions.ModelsClient.get_by_name", side_effect=HTTPError
    ), patch("giza.commands.versions.get_response_info", return_value={}), patch(
        "giza.commands.versions.Path"
    ), patch.object(
        VersionsClient, "_load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["versions", "transpile", "model", "--output-path", tmpdir],
            expected_error=True,
        )

    assert "Error at transpilation" in result.stdout
    assert result.exit_code == 1


# Test version transpilation with bad zip file
def test_versions_transpile_bad_zip(tmpdir):
    def return_content():
        return b"some bytes"

    models = ModelList(
        __root__=[
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
    )

    with patch(
        "giza.commands.versions.VersionsClient",
        return_value=ClientStub(version, return_content()),
    ), patch(
        "giza.commands.versions.ModelsClient.list",
        return_value=models,
    ), patch(
        "giza.commands.versions.Path"
    ), patch.object(
        VersionsClient, "get", return_value=version
    ), patch(
        "builtins.open"
    ) as mock_open, patch.object(
        VersionsClient, "_load_credentials_file"
    ), patch(
        "giza.commands.versions.ModelsClient._load_credentials_file"
    ):
        result = invoke_cli_runner(
            ["versions", "transpile", "model", "--output-path", tmpdir],
            expected_error=True,
        )

    # Called twice, once to open the model and second to write the zip
    mock_open.assert_called()
    assert "Something went wrong" in result.stdout
    assert "Error ->" in result.stdout
    assert result.exit_code == 1


# Test successful version download
def test_versions_download_successful(tmpdir):
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
    )

    def return_content():
        tmp = BytesIO()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr("file1.txt", "hi")
        return tmp.getvalue()

    with patch.object(VersionsClient, "get", return_value=version), patch.object(
        VersionsClient, "download", return_value=return_content()
    ), patch("builtins.open") as mock_open, patch(
        "giza.client.VersionsClient._load_credentials_file"
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
    assert "Transpilation is ready, downloading!" in result.stdout
    assert result.exit_code == 0


# Test version download with server error
def test_versions_download_server_error():
    with patch.object(VersionsClient, "get", side_effect=HTTPError), patch(
        "giza.commands.versions.get_response_info", return_value={}
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
    assert "Error at download" in result.stdout


# Test version download with bad zip file
def test_versions_download_bad_zip(tmpdir):
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
    )

    def return_content():
        return b"some bytes"

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

    assert "Something went wrong with the transpiled file" in result.stdout
    assert result.exit_code == 1


# Test version download with missing model_id and version_id
def test_versions_download_missing_ids():
    with patch.object(VersionsClient, "get", side_effect=HTTPError), patch(
        "giza.commands.versions.get_response_info", return_value={}
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
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
    )

    with patch.object(VersionsClient, "update", return_value=version):
        result = invoke_cli_runner(
            [
                "versions",
                "update",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--description",
                "updated_description",
            ]
        )

    assert "Updating version description" in result.stdout
    assert result.exit_code == 0
    assert "updated_description" in result.stdout


def test_versions_update_server_error():
    with patch.object(VersionsClient, "update", side_effect=HTTPError), patch(
        "giza.commands.versions.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "update",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--description",
                "updated_description",
            ],
            expected_error=True,
        )

    assert "Could not update version" in result.stdout
    assert result.exit_code == 1


def test_versions_update_missing_ids():
    with patch.object(VersionsClient, "update", side_effect=HTTPError), patch(
        "giza.commands.versions.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            [
                "versions",
                "update",
                "--description",
                "updated_description",
            ],
            expected_error=True,
        )

    assert (
        "Model ID, version ID and description are required to update the version"
        in result.stdout
    )
    assert result.exit_code == 1
