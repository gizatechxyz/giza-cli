from unittest.mock import patch

from requests import HTTPError

from giza.commands.deployments import DeploymentsClient, cairo
from giza.frameworks import ezkl
from giza.schemas.deployments import Deployment, DeploymentsList
from tests.conftest import invoke_cli_runner


def test_deploy_with_cairo_framework():
    with patch.object(cairo, "deploy") as mock_deploy:
        result = invoke_cli_runner(
            [
                "deployments",
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
                "deployments",
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
    deploy_list = DeploymentsList(
        __root__=[
            Deployment(
                id=1,
                status="COMPLETED",
                uri="https://giza-api.com/deployments/1",
                size="S",
                service_name="giza-deployment-1",
                model_id=1,
                version_id=1,
            ),
        ]
    )
    with patch.object(
        DeploymentsClient, "list", return_value=deploy_list
    ) as mock_deploy:
        result = invoke_cli_runner(
            [
                "deployments",
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
            "deployments",
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
    deployments_list = DeploymentsList(
        __root__=[
            Deployment(
                id=1,
                status="COMPLETED",
                uri="https://giza-api.com/deployments/1",
                size="S",
                service_name="giza-deployment-1",
                model_id=1,
                version_id=1,
            ),
            Deployment(
                id=2,
                status="COMPLETED",
                uri="https://giza-api.com/deployments/2",
                size="S",
                service_name="giza-deployment-2",
                model_id=1,
                version_id=1,
            ),
        ]
    )
    with patch.object(
        DeploymentsClient, "list", return_value=deployments_list
    ) as mock_list:
        result = invoke_cli_runner(
            ["deployments", "list", "--model-id", "1", "--version-id", "1"],
        )
    mock_list.assert_called_once()
    assert result.exit_code == 0
    assert "giza-deployment-1" in result.stdout
    assert "giza-deployment-2" in result.stdout


def test_list_deployments_http_error():
    with patch.object(DeploymentsClient, "list", side_effect=HTTPError):
        result = invoke_cli_runner(
            ["deployments", "list", "--model-id", "1", "--version-id", "1"],
            expected_error=True,
        )
    assert result.exit_code == 1
    assert "Could not list deployments" in result.stdout


def test_get_deployment():
    deployment = Deployment(
        id=1,
        status="COMPLETED",
        uri="https://giza-api.com/deployments/1",
        size="S",
        service_name="giza-deployment-1",
        model_id=1,
        version_id=1,
    )
    with patch.object(
        DeploymentsClient, "get", return_value=deployment
    ) as mock_deployment:
        result = invoke_cli_runner(
            [
                "deployments",
                "get",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--deployment-id",
                "1",
            ],
        )
    mock_deployment.assert_called_once()
    assert result.exit_code == 0
    assert "giza-deployment-1" in result.stdout


def test_get_deployment_http_error():
    with patch.object(
        DeploymentsClient, "get", side_effect=HTTPError
    ) as mock_deployment:
        result = invoke_cli_runner(
            [
                "deployments",
                "get",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--deployment-id",
                "1",
            ],
            expected_error=True,
        )
    mock_deployment.assert_called_once()
    assert result.exit_code == 1
    assert "Could not get deployment" in result.stdout
