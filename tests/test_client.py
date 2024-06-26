import datetime
import json
from io import BufferedReader
from unittest.mock import MagicMock, Mock, patch

import pytest
from jose import ExpiredSignatureError
from requests import HTTPError

from giza.cli.client import (
    DEFAULT_API_VERSION,
    MODEL_URL_HEADER,
    ApiClient,
    JobsClient,
    ModelsClient,
    ProofsClient,
    VersionsClient,
)
from giza.cli.schemas.jobs import Job, JobCreate
from giza.cli.schemas.models import Model, ModelCreate, ModelUpdate
from giza.cli.schemas.proofs import Proof
from giza.cli.schemas.versions import Version, VersionCreate, VersionList
from giza.cli.utils.enums import Framework, JobSize, JobStatus, VersionStatus


class ResponseStub:
    def __init__(
        self, data, status_code, exception=None, headers=None, content=None
    ) -> None:
        self.status_code = status_code
        self.data = data
        self.exception = exception
        self.headers = headers
        self.content = content

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


def test_models_client_get(tmpdir):
    model_data = {
        "name": "model",
        "size": 100,
        "status": "COMPLETED",
        "message": "",
        "id": 1,
    }
    model_id = 1
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=ResponseStub(model_data, 200)
    ) as mock_request, patch("jose.jwt.decode"):
        client = ModelsClient("http://dummy_host", token="token")
        model = client.get(model_id)

    mock_request.assert_called_once()
    assert isinstance(model, Model)


def test_models_client_create(tmpdir):
    model_create = ModelCreate(description="Dummy Model", name="model")
    model_data = {
        "name": "model",
        "description": "Dummy Model",
        "id": 1,
    }
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.post",
        return_value=ResponseStub(
            model_data,
            201,
        ),
    ) as mock_request, patch("jose.jwt.decode"):
        client = ModelsClient("http://dummy_host", token="token")
        model = client.create(model_create)

    mock_request.assert_called_once()
    assert isinstance(model, Model)
    assert model.name == model_create.name


def test_models_client_update(tmpdir):
    model_update = ModelUpdate(description="Updated Desc")
    model_data = {
        "name": "model",
        "description": "Updated Desc",
        "id": 1,
    }
    model_id = 1
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.put",
        return_value=ResponseStub(
            model_data,
            200,
        ),
    ) as mock_request, patch("jose.jwt.decode"):
        client = ModelsClient("http://dummy_host", token="token")
        model = client.update(model_id, model_update)

    mock_request.assert_called_once()
    assert isinstance(model, Model)
    assert model.description == model_update.description


def test_models_client_list(tmpdir):
    model_data = {
        "name": "model",
        "description": "Dummy Model",
        "id": 1,
    }
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get",
        return_value=ResponseStub(
            [model_data],
            200,
        ),
    ) as mock_request, patch("jose.jwt.decode"):
        client = ModelsClient("http://dummy_host", token="token")
        models = client.list()

    mock_request.assert_called_once()
    assert isinstance(models.root[0], Model)
    assert models.root[0].name == model_data["name"]


def test_models_client_get_non_existent(tmpdir):
    model_id = 999
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", side_effect=HTTPError
    ) as mock_request, patch("jose.jwt.decode"):
        client = ModelsClient("http://dummy_host", token="token")
        with pytest.raises(HTTPError):
            client.get(model_id)

    mock_request.assert_called_once()


def test_models_client_update_non_existent(tmpdir):
    model_update = ModelUpdate(description="Updated Desc")
    model_id = 999
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.put",
        side_effect=HTTPError,
    ) as mock_request, patch("jose.jwt.decode"):
        client = ModelsClient("http://dummy_host", token="token")
        with pytest.raises(HTTPError):
            client.update(model_id, model_update)

    mock_request.assert_called_once()


def test_versions_client_get(tmpdir):
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.STARTING,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )
    response = ResponseStub(version.model_dump(), 200)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        client = VersionsClient("http://dummy_host", token="token")
        result = client.get(model_id=1, version_id=version.version)

    mock_request.assert_called()
    assert version == result


def test_versions_client_list(tmpdir):
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.COMPLETED,
        created_date="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
        last_update="2021-08-31T15:00:00.000000",
    )
    response = ResponseStub([version.model_dump()], 200)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        client = VersionsClient("http://dummy_host", token="token")
        result = client.list(model_id=1)

    mock_request.assert_called()
    assert version == result.root[0]
    assert isinstance(result, VersionList)


def test_versions_client_create(tmpdir):
    version = Version(
        version=1,
        size=1,
        description="test_version",
        status=VersionStatus.STARTING,
        created_date="2021-08-31T15:00:00.000000",
        last_update="2021-08-31T15:00:00.000000",
        framework=Framework.CAIRO,
    )
    response = ResponseStub(
        version.model_dump(), 201, headers={MODEL_URL_HEADER.lower(): "url"}
    )
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.post", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        filename = "test.onnx"
        client = VersionsClient("http://dummy_host", token="token")
        version_create = VersionCreate(
            status=VersionStatus.STARTING, size=100, framework=Framework.CAIRO
        )
        result, url = client.create(
            model_id=1, version_create=version_create, filename=filename
        )

    mock_request.assert_called()
    assert version == result
    assert url == "url"


def test_versions_client_get_non_existent(tmpdir):
    version_id = 999
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", side_effect=HTTPError
    ) as mock_request, patch("jose.jwt.decode"):
        client = VersionsClient("http://dummy_host", token="token")
        with pytest.raises(HTTPError):
            client.get(model_id=1, version_id=version_id)

    mock_request.assert_called_once()


def test_jobs_client_get(tmpdir):
    job_id = 1
    job = Job(id=1, job_name="job", size=JobSize.S, status=JobStatus.STARTING)
    response = ResponseStub(job.model_dump(), 200)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        client = JobsClient("http://dummy_host", token="token")
        result = client.get(job_id)

    mock_request.assert_called()
    assert job == result


def test_jobs_client_list(tmpdir):
    job = Job(id=1, job_name="job", size=JobSize.S, status=JobStatus.STARTING)
    response = ResponseStub([job.model_dump()], 200)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        client = JobsClient("http://dummy_host", token="token")
        result = client.list()

    mock_request.assert_called()
    assert job == result[0]


def test_jobs_client_create(tmpdir):
    job = Job(id=1, job_name="job", size=JobSize.S, status=JobStatus.STARTING)
    response = ResponseStub(job.model_dump(), 201)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.post", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        mock = Mock(BufferedReader)
        client = JobsClient("http://dummy_host", token="token")
        job_create = JobCreate(size=JobSize.S)
        result = client.create(job_create, mock)

    mock_request.assert_called()
    assert job == result


def test_proof_client_get(tmpdir):
    proof_id = 1
    proof = Proof(
        id=1,
        job_id=1,
        proving_time=100,
        cairo_execution_time=100,
        created_date=datetime.datetime.now(),
    )
    response = ResponseStub(proof.model_dump(), 200)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        client = ProofsClient("http://dummy_host", token="token")
        result = client.get(proof_id)

    mock_request.assert_called()
    assert proof == result


def test_proof_client_get_by_job_id(tmpdir):
    job_id = 1
    proof = Proof(
        id=1,
        job_id=1,
        proving_time=100,
        cairo_execution_time=100,
        created_date=datetime.datetime.now(),
    )
    response = ResponseStub([proof.model_dump()], 200)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        client = ProofsClient("http://dummy_host", token="token")
        result = client.get_by_job_id(job_id)

    mock_request.assert_called()
    assert proof == result
    assert job_id == result.job_id


def test_proof_client_list(tmpdir):
    proof = Proof(
        id=1,
        job_id=1,
        proving_time=100,
        cairo_execution_time=100,
        created_date=datetime.datetime.now(),
    )
    response = ResponseStub([proof.model_dump()], 200)
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", return_value=response
    ) as mock_request, patch("jose.jwt.decode"):
        client = ProofsClient("http://dummy_host", token="token")
        result = client.list()

    mock_request.assert_called()
    assert proof == result[0]


def test_proof_client_download(tmpdir):
    proof_id = 1
    response_download = ResponseStub({"download_url": "url"}, 200)
    response_url = ResponseStub(None, 200, content=b"some bytes")
    with patch("pathlib.Path.home", return_value=tmpdir), patch(
        "requests.Session.get", side_effect=[response_download, response_url]
    ) as mock_request, patch("jose.jwt.decode"):
        client = ProofsClient("http://dummy_host", token="token")
        result = client.download(proof_id)

    mock_request.assert_called()
    assert isinstance(result, bytes)
