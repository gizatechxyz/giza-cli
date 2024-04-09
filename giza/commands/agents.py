import sys
from enum import StrEnum
from typing import List, Optional

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

from giza import API_HOST
from giza.client import AgentsClient, EndpointsClient
from giza.options import DEBUG_OPTION
from giza.schemas.agents import AgentCreate, AgentList, AgentUpdate
from giza.utils import echo
from giza.utils.exception_handling import ExceptionHandler
from giza.utils.misc import get_ape_accounts, get_parameters_from_str, load_json_file

app = typer.Typer()


@app.command(
    short_help="🕵️‍♂️ Creates an agent to interact with smart contracts",
    help="""🕵️‍♂️ Creates an agent to interact with smart contracts.

    This command will create an agent to use in Giza. The agent is used to interact with smart contracts and perform inference requests.
    The agent will handle the communication between the user account (wallet) and the smart contract, while also providing the handling of proof verification.
    """,
)
def create(
    model_id: int = typer.Option(
        None,
        "--model-id",
        "-m",
        help="The ID of the model used to create the agent",
    ),
    version_id: int = typer.Option(
        None,
        "--version-id",
        "-v",
        help="The ID of the version used to create the agent",
    ),
    endpoint_id: int = typer.Option(
        None,
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint used to create the agent",
    ),
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="The name of the agent"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="The description of the agent"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo("Creating agent ✅ ")

    if not model_id and not version_id and not endpoint_id:
        echo.error("Please provide a model id and version id or endpoint id")
        sys.exit(1)
    elif endpoint_id:
        echo.info(
            "Using endpoint id to create agent, retrieving model id and version id"
        )
        endpoints_client = EndpointsClient(API_HOST)
        endpoint = endpoints_client.get(endpoint_id)
        model_id = endpoint.model_id
        version_id = endpoint.version_id
    elif model_id and version_id:
        echo.info("Using model id and version id to create agent")
        endpoints_client = EndpointsClient(API_HOST)
        endpoint = endpoints_client.list(
            params={"model_id": model_id, "version_id": version_id}
        ).root[0]
        endpoint_id = endpoint.id
    with ExceptionHandler(debug=debug):
        client = AgentsClient(API_HOST)
        available_accounts = get_ape_accounts()
        if available_accounts == {}:
            echo.error(
                "No available accounts found. Please create an account first running `ape accounts generate <ALIAS>`."
            )
            sys.exit(1)
        table = Table()

        table.add_column("Accounts", justify="center", style="orange3")
        for account in available_accounts:
            table.add_row(account)

        echo.info("Select an existing account to create the agent.")
        echo.info("Available accounts are:")
        console = Console()
        console.print(table)

        accounts_enum = StrEnum(  # type: ignore
            "Accounts", {account: account for account in available_accounts}
        )
        selected_account = typer.prompt("Enter the account name", type=accounts_enum)

        keyfile = load_json_file(str(available_accounts.get(selected_account)))

        agent_create = AgentCreate(
            name=name,
            description=description,
            parameters={
                "model_id": model_id,
                "version_id": version_id,
                "endpoint_id": endpoint_id,
                "alias": selected_account,
                "account_data": keyfile,
            },
        )
        agent = client.create(agent_create)
    print_json(agent.model_dump_json())


@app.command(
    short_help="📜 List the available agents.",
    help="""📜 Lists all the available agents in Giza.
    This command retrieves and displays a list of all agents stored in the server.

    To filter by parameters, use the `--parameters` flag. The parameters should be provided in the format `key=value`.
    Example: `--parameters key1=value1 --parameters key2=value2`

    Each agent information is printed in a json format for easy readability and further processing.
    If there are no agents available, an empty list is printed.
    """,
)
def list(
    parameters: Optional[List[str]] = typer.Option(
        None, "--parameters", "-p", help="The parameters of the agent"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo("Listing agents ✅ ")
    with ExceptionHandler(debug=debug):
        client = AgentsClient(API_HOST)
        q = get_parameters_from_str(parameters) if parameters else None
        if q:
            echo(f"Filtering agents with parameters: {q}")
            query_params = {"q": [f"{k}=={v}" for k, v in q.items()]}
        else:
            query_params = None
        agents: AgentList = client.list(params=query_params)
    print_json(agents.model_dump_json())


# giza/commands/deployments.py
@app.command(
    short_help="🎯 Get an agent.",
    help="""🎯 Get a specific agent in Giza.
    This command retrieves and displays a specific agent stored in the server.
    The agent information is printed in a json format for easy readability and further processing.
    If the agent is not available, an error message is printed.
    """,
)
def get(
    agent_id: int = typer.Option(
        None,
        "--agent-id",
        "-a",
        help="The ID of the agent",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Getting agent {agent_id} ✅ ")
    with ExceptionHandler(debug=debug):
        client = AgentsClient(API_HOST)
        deployment = client.get(agent_id)
    print_json(deployment.model_dump_json())


@app.command(
    name="delete",
    short_help="🗑️ Deletes an agent.",
    help="""🗑️ Deletes an agent and erases all the metadata from Giza.

    This command will remove the `agent` metadata from Giza. The agent will no longer be available for use.
    """,
)
def delete_agent(
    agent_id: int = typer.Option(
        None,
        "--agent-id",
        "-a",
        help="The ID of the agent",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Deleting agent {agent_id} ✅ ")
    with ExceptionHandler(debug=debug):
        client = AgentsClient(API_HOST)
        client.delete(agent_id)
    echo(f"Agent {agent_id} deleted ✅ ")


@app.command(
    short_help="🔄 Updates an agent.",
    help="""🔄 Updates an agent in Giza.

    This command will update the agent metadata in Giza. The agent information will be updated with the provided parameters.

    To update the parameters, use the `--parameters` flag. The parameters should be provided in the format `key=value`.
    Example: `--parameters key1=value1 --parameters key2=value2`

    The updated agent information is printed in a json format for easy readability and further processing.
    """,
)
def update(
    agent_id: int = typer.Option(
        None,
        "--agent-id",
        "-a",
        help="The ID of the agent",
    ),
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="The name of the agent"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="The description of the agent"
    ),
    parameters: Optional[List[str]] = typer.Option(
        None, "--parameters", "-p", help="The parameters of the agent"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Updating agent {agent_id} ✅ ")
    with ExceptionHandler(debug=debug):
        client = AgentsClient(API_HOST)
        update_params = get_parameters_from_str(parameters) if parameters else None
        agent_update = AgentUpdate(
            name=name, description=description, parameters=update_params
        )
        agent = client.patch(agent_id, agent_update)
    print_json(agent.model_dump_json())
