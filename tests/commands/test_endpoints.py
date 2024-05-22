from unittest.mock import patch

from requests import HTTPError

from giza.cli.commands.endpoints import EndpointsClient, cairo
from giza.cli.frameworks import ezkl
from giza.cli.schemas.endpoints import Endpoint, EndpointsList
from giza.cli.schemas.verify import VerifyResponse
from tests.conftest import invoke_cli_runner


def test_deploy_with_cairo_framework():
    with patch.object(cairo, "deploy") as mock_deploy:
        result = invoke_cli_runner(
            [
                "endpoints",
                "deploy",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--framework",
                "CAIRO",
                "--size",
                "S",
                "--debug",
                "data_path",
            ]
        )
    mock_deploy.assert_called_once()
    assert result.exit_code == 0


def test_deploy_with_ezkl_framework():
    with patch.object(ezkl, "deploy") as mock_deploy:
        result = invoke_cli_runner(
            [
                "endpoints",
                "deploy",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--framework",
                "EZKL",
                "--size",
                "S",
                "data_path",
            ],
        )
    mock_deploy.assert_called_once()
    assert result.exit_code == 0


def test_deploy_ezkl_existing_deployment():
    deploy_list = EndpointsList(
        root=[
            Endpoint(
                id=1,
                status="COMPLETED",
                uri="https://giza-api.com/deployments/1",
                size="S",
                service_name="giza-deployment-1",
                model_id=1,
                version_id=1,
                is_active=True,
            ),
        ]
    )
    with patch.object(EndpointsClient, "list", return_value=deploy_list) as mock_deploy:
        result = invoke_cli_runner(
            [
                "endpoints",
                "deploy",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--framework",
                "EZKL",
                "--size",
                "S",
                "data_path",
            ],
            expected_error=True,
        )
    mock_deploy.assert_called_once()
    assert "already exists" in result.stdout


def test_deploy_with_unsupported_framework():
    result = invoke_cli_runner(
        [
            "endpoints",
            "deploy",
            "--model-id",
            "1",
            "--version-id",
            "1",
            "--framework",
            "NONEXISTING",
            "--size",
            "S",
            "data_path",
        ],
        expected_error=True,
    )
    assert result.exit_code == 2


def test_list_deployments():
    deployments_list = EndpointsList(
        root=[
            Endpoint(
                id=1,
                status="COMPLETED",
                uri="https://giza-api.com/deployments/1",
                size="S",
                service_name="giza-deployment-1",
                model_id=1,
                version_id=1,
                is_active=True,
            ),
            Endpoint(
                id=2,
                status="COMPLETED",
                uri="https://giza-api.com/deployments/2",
                size="S",
                service_name="giza-deployment-2",
                model_id=1,
                version_id=1,
                is_active=True,
            ),
        ]
    )
    with patch.object(
        EndpointsClient, "list", return_value=deployments_list
    ) as mock_list:
        result = invoke_cli_runner(
            ["endpoints", "list", "--model-id", "1", "--version-id", "1"],
        )
    mock_list.assert_called_once()
    assert result.exit_code == 0
    assert "giza-deployment-1" in result.stdout
    assert "giza-deployment-2" in result.stdout


def test_create_deployments_empty():
    deployments_list = EndpointsList(root=[])
    with patch.object(
        EndpointsClient, "list", return_value=deployments_list
    ) as mock_list, patch.object(
        EndpointsClient,
        "create",
        return_value=Endpoint(
            id=1,
            status="COMPLETED",
            uri="https://giza-api.com/deployments/1",
            size="S",
            service_name="giza-deployment-1",
            model_id=1,
            version_id=1,
            is_active=True,
        ),
    ):
        result = invoke_cli_runner(
            ["endpoints", "deploy", "--model-id", "1", "--version-id", "1"],
        )
    mock_list.assert_called_once()
    assert result.exit_code == 0
    assert "Endpoint is successful" in result.stdout
    assert "https://giza-api.com/deployments/1" in result.stdout


def test_list_deployments_http_error():
    with patch.object(EndpointsClient, "list", side_effect=HTTPError):
        result = invoke_cli_runner(
            ["endpoints", "list", "--model-id", "1", "--version-id", "1"],
            expected_error=True,
        )
    assert result.exit_code == 1
    assert "Could not list endpoints" in result.stdout


def test_get_deployment():
    deployment = Endpoint(
        id=1,
        status="COMPLETED",
        uri="https://giza-api.com/deployments/1",
        size="S",
        service_name="giza-deployment-1",
        model_id=1,
        version_id=1,
        is_active=True,
    )
    with patch.object(
        EndpointsClient, "get", return_value=deployment
    ) as mock_deployment:
        result = invoke_cli_runner(
            [
                "endpoints",
                "get",
                "--endpoint-id",
                "1",
            ],
        )
    mock_deployment.assert_called_once()
    assert result.exit_code == 0
    assert "giza-deployment-1" in result.stdout


def test_get_deployment_http_error():
    with patch.object(EndpointsClient, "get", side_effect=HTTPError) as mock_deployment:
        result = invoke_cli_runner(
            [
                "endpoints",
                "get",
                "--endpoint-id",
                "1",
            ],
            expected_error=True,
        )
    mock_deployment.assert_called_once()
    assert result.exit_code == 1
    assert "Could not get endpoint" in result.stdout


def test_endpoints_verify():
    with patch.object(
        EndpointsClient,
        "verify_proof",
        return_value=VerifyResponse(verification=True, verification_time=1.2),
    ) as mock_verify:
        result = invoke_cli_runner(
            [
                "endpoints",
                "verify",
                "--endpoint-id",
                "1",
                "--proof-id",
                "1",
            ],
        )
    mock_verify.assert_called_once()
    assert result.exit_code == 0
    assert ' "verification": true' in result.stdout
