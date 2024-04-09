from pathlib import Path
from unittest.mock import patch

from giza.commands.agents import AgentsClient, EndpointsClient
from giza.schemas.agents import Agent, AgentList, AgentUpdate
from giza.schemas.endpoints import Endpoint
from tests.conftest import invoke_cli_runner


def test_get_agent():
    """
    Test the `get` command of the `agents` command group.
    """

    agent = Agent(
        id=1,
        name="test agent",
        description="test",
        parameters={},
    )
    with patch.object(AgentsClient, "get", return_value=agent) as mock_get:
        result = invoke_cli_runner(
            [
                "agents",
                "get",
                "--agent-id",
                "1",
            ]
        )
    mock_get.assert_called_once()
    assert result.exit_code == 0
    assert "test agent" in result.output


def test_create_agent_with_model_id_and_version_id():
    """
    Test the `create` command of the `agents` command group with model id and version id.
    """

    agent = Agent(
        id=1,
        name="test agent",
        description="test",
        parameters={},
    )
    with patch.object(AgentsClient, "create", return_value=agent) as mock_create, patch(
        "giza.commands.agents.get_ape_accounts",
        return_value={"test": Path("dummy.json")},
    ) as mock_accounts, patch(
        "typer.prompt", side_effect=["test"]
    ) as mock_prompt, patch(
        "giza.commands.agents.load_json_file", return_value={}
    ) as mock_load:
        result = invoke_cli_runner(
            [
                "agents",
                "create",
                "--model-id",
                "1",
                "--version-id",
                "1",
                "--name",
                "test agent",
                "--description",
                "test",
            ]
        )
    mock_create.assert_called_once()
    mock_accounts.assert_called_once()
    mock_prompt.assert_called_once()
    mock_load.assert_called_once()
    assert result.exit_code == 0
    assert "Using model id and version id to create agent" in result.output
    assert "test agent" in result.output


def test_create_agent_with_endpoint_id():
    """
    Test the `create` command of the `agents` command group with model id and version id.
    """

    agent = Agent(
        id=1,
        name="test agent endpoint",
        description="test",
        parameters={},
    )
    with patch.object(AgentsClient, "create", return_value=agent) as mock_create, patch(
        "giza.commands.agents.get_ape_accounts",
        return_value={"test": Path("dummy.json")},
    ) as mock_accounts, patch(
        "typer.prompt", side_effect=["test"]
    ) as mock_prompt, patch(
        "giza.commands.agents.load_json_file", return_value={}
    ) as mock_load, patch.object(
        EndpointsClient,
        "get",
        return_value=Endpoint(id=1, size="S", model_id=1, version_id=1, is_active=True),
    ) as mock_endpoints:
        result = invoke_cli_runner(
            [
                "agents",
                "create",
                "--endpoint-id",
                "1",
                "--name",
                "test agent endpoint",
                "--description",
                "test",
            ]
        )
    mock_create.assert_called_once()
    mock_accounts.assert_called_once()
    mock_prompt.assert_called_once()
    mock_load.assert_called_once()
    mock_endpoints.assert_called_once()
    assert result.exit_code == 0
    assert "Using endpoint id to create agent" in result.output
    assert "test agent endpoint" in result.output


def test_create_agent_no_ids():
    """
    Test the `create` command of the `agents` command group with model id and version id.
    """
    result = invoke_cli_runner(
        [
            "agents",
            "create",
            "--name",
            "test agent",
            "--description",
            "test",
        ],
        expected_error=True,
    )
    assert result.exit_code == 1
    assert "Please provide a model id and version id or endpoint id" in result.output


def test_list_agents():
    """
    Test the `list` command of the `agents` command group.
    """

    agents = AgentList(
        root=[
            Agent(
                id=1,
                name="test agent",
                description="test",
                parameters={},
            ),
            Agent(
                id=2,
                name="test agent 2",
                description="test",
                parameters={},
            ),
        ]
    )
    with patch.object(AgentsClient, "list", return_value=agents) as mock_list:
        result = invoke_cli_runner(
            [
                "agents",
                "list",
            ]
        )

    mock_list.assert_called_once()
    assert result.exit_code == 0
    assert "test agent" in result.output
    assert "test agent 2" in result.output


def test_list_agents_with_params():
    """
    Test the `list` command of the `agents` command group.
    """

    agents = AgentList(
        root=[
            Agent(
                id=1,
                name="test agent",
                description="test",
                parameters={
                    "account": "test",
                },
            ),
        ]
    )
    with patch.object(AgentsClient, "list", return_value=agents) as mock_list:
        result = invoke_cli_runner(
            [
                "agents",
                "list",
                "--parameters",
                "account=test",
            ]
        )

    mock_list.assert_called_once_with(params={"q": ["account==test"]})
    assert result.exit_code == 0
    assert "test agent" in result.output


def test_delete_agent():
    """
    Test the `delete` command of the `agents` command group.
    """

    with patch.object(AgentsClient, "delete") as mock_delete:
        result = invoke_cli_runner(
            [
                "agents",
                "delete",
                "--agent-id",
                "1",
            ]
        )
    mock_delete.assert_called_once()
    assert result.exit_code == 0
    assert "Agent 1 deleted" in result.output


def test_update_agent():
    """
    Test the `update` command of the `agents` command group.
    """

    agent = Agent(
        id=1,
        name="updated agent",
        description="test",
        parameters={},
    )
    with patch.object(AgentsClient, "patch", return_value=agent) as mock_patch:
        result = invoke_cli_runner(
            [
                "agents",
                "update",
                "--agent-id",
                "1",
                "--name",
                "test agent",
                "--description",
                "test",
            ]
        )
    mock_patch.assert_called_once()
    assert result.exit_code == 0
    assert "updated agent" in result.output


def test_update_agent_with_parameters():
    """
    Test the `update` command of the `agents` command group.
    """

    agent = Agent(
        id=1,
        name="test agent",
        description="test",
        parameters={
            "account": "test",
        },
    )
    with patch.object(AgentsClient, "patch", return_value=agent) as mock_patch:
        result = invoke_cli_runner(
            [
                "agents",
                "update",
                "--agent-id",
                "1",
                "--name",
                "test agent",
                "--description",
                "test",
                "--parameters",
                "account=test",
            ]
        )
    mock_patch.assert_called_once_with(
        1,
        AgentUpdate(
            name="test agent", description="test", parameters={"account": "test"}
        ),
    )
    assert result.exit_code == 0
    assert "test agent" in result.output
    assert "account" in result.output
