from unittest.mock import patch

import pytest
from requests import HTTPError

from giza.commands.workspaces import WorkspaceClient
from giza.schemas.workspaces import Workspace
from tests.conftest import invoke_cli_runner


# Test successful workspace creation
@pytest.mark.parametrize("debug", ["", "--debug"])
def test_workspaces_create(debug):
    workspace = Workspace(
        status="STARTING",
    )
    workspace_done = Workspace(
        url="https://gizatech.xyz",
        status="COMPLETED",
    )
    with patch.object(
        WorkspaceClient, "create", return_value=workspace
    ) as mock_create, patch.object(
        WorkspaceClient, "get", return_value=workspace_done
    ) as mock_get, patch(
        "giza.commands.workspaces.time.sleep"
    ):
        args = (
            ["workspaces", "create"] if not debug else ["workspaces", "create", debug]
        )
        result = invoke_cli_runner(args)

    assert result.exit_code == 0
    mock_create.assert_called_once()
    mock_get.assert_called_once()
    assert "Worksace creation is successful" in result.stdout


# Test workspaces creation when a workspace already exists
@pytest.mark.parametrize("debug", ["", "--debug"])
def test_workspaces_create_http_error(debug):
    with patch.object(WorkspaceClient, "create", side_effect=HTTPError):
        args = (
            ["workspaces", "create"] if not debug else ["workspaces", "create", debug]
        )
        result = invoke_cli_runner(args, expected_error=True)

    assert result.exit_code == 1
    assert "Could not create the workspace" in result.stdout


# Test successful workspaces get
@pytest.mark.parametrize("debug", ["", "--debug"])
def test_workspace_get(debug):
    workspace = Workspace(
        url="https://gizatech.xyz",
        status="COMPLETED",
    )
    with patch.object(WorkspaceClient, "get", return_value=workspace) as mock_get:
        args = ["workspaces", "get"] if not debug else ["workspaces", "get", debug]
        result = invoke_cli_runner(args, expected_error=True)

    assert result.exit_code == 0
    mock_get.assert_called_once()
    assert "Workspace URL: https://gizatech.xyz" in result.stdout


# Test successful workspaces error handling on get
@pytest.mark.parametrize("debug", ["", "--debug"])
def test_workspace_get_error(debug):
    with patch.object(WorkspaceClient, "get", side_effect=HTTPError) as mock_get:
        args = ["workspaces", "get"] if not debug else ["workspaces", "get", debug]
        result = invoke_cli_runner(args, expected_error=True)

    assert result.exit_code == 1
    mock_get.assert_called_once()
    assert "There is an error retrieving the workspace information" in result.stdout


# Test successful workspaces delete with yes
@pytest.mark.parametrize("debug", ["", "--debug"])
def test_workspace_delete_yes(debug):
    with patch.object(WorkspaceClient, "delete") as mock_delete, patch(
        "typer.confirm", return_value=True
    ):
        args = (
            ["workspaces", "delete"] if not debug else ["workspaces", "delete", debug]
        )
        result = invoke_cli_runner(args)

    assert result.exit_code == 0
    mock_delete.assert_called_once()
    assert "Deleting Workspace" in result.stdout
    assert "Workspace Deleted" in result.stdout


# Test successful workspaces delete with no
@pytest.mark.parametrize("debug", ["", "--debug"])
def test_workspace_delete_no(debug):
    with patch("typer.confirm", return_value=False):
        args = (
            ["workspaces", "delete"] if not debug else ["workspaces", "delete", debug]
        )
        result = invoke_cli_runner(args)

    assert result.exit_code == 0
    assert "Aborting" in result.stdout


# Test deleting error
@pytest.mark.parametrize("debug", ["", "--debug"])
def test_workspace_delete_error(debug):
    with patch.object(
        WorkspaceClient, "delete", side_effect=HTTPError
    ) as mock_get, patch("typer.confirm", return_value=True):
        args = (
            ["workspaces", "delete"] if not debug else ["workspaces", "delete", debug]
        )
        result = invoke_cli_runner(args, expected_error=True)

    assert result.exit_code == 1
    mock_get.assert_called_once()
    assert "There is an error while deleting workspace" in result.stdout
