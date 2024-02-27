import sys
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError
from rich import print_json

from giza import API_HOST
from giza.client import EndpointsClient
from giza.frameworks import cairo, ezkl
from giza.options import DEBUG_OPTION
from giza.schemas.deployments import EndpointsList
from giza.schemas.proofs import Proof, ProofList
from giza.utils import echo, get_response_info
from giza.utils.enums import Framework, ServiceSize

app = typer.Typer()


def deploy(
    data: str = typer.Argument(None),
    model_id: int = typer.Option(
        None,
        "--model-id",
        "-m",
        help="The ID of the model where an endpoint will be created",
    ),
    version_id: int = typer.Option(
        None,
        "--version-id",
        "-v",
        help="The ID of the version that will used in the endpoint",
    ),
    size: ServiceSize = typer.Option(ServiceSize.S, "--size", "-s"),
    framework: Framework = typer.Option(Framework.CAIRO, "--framework", "-f"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if framework == Framework.CAIRO:
        cairo.deploy(
            data=data, model_id=model_id, version_id=version_id, size=size, debug=debug
        )
    elif framework == Framework.EZKL:
        ezkl.deploy(model_id=model_id, version_id=version_id, size=size, debug=debug)
    else:
        raise typer.BadParameter(
            f"Framework {framework} is not supported, please use one of the following: {Framework.CAIRO}, {Framework.EZKL}"
        )


app.command(
    short_help="🚀 Creates an endpoint for the specified model version.",
    help="""🚀 Creates an endpoint for the specified model version.

    This command will create an inference endpoint in Giza for the available frameworks.

    This command performs several operations:

        * Creates an endpoint for the specified version
        * Uploads the specified version file
        * Polls the version until the status is either FAILED or COMPLETED
        * If the status is COMPLETED, sends back the endpoint url to make inference requests

    Error handling is also incorporated into this process.
    """,
)(deploy)


@app.command(
    short_help="📜 List the available endpoints.",
    help="""📜 Lists all the available endpoints in Giza.
    This command retrieves and displays a list of all endpoints stored in the server.
    Each endpoint information is printed in a json format for easy readability and further processing.
    If there are no endpoints available, an empty list is printed.
    """,
)
def list(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo("Listing endpoints ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        deployments: EndpointsList = client.list(model_id, version_id)
    except ValidationError as e:
        echo.error("Endpoint validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not list endpoints")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(deployments.json())


# giza/commands/deployments.py
@app.command(
    short_help="🎯 Get an endpoint.",
    help="""🎯 Get a specific endpoint in Giza.
    This command retrieves and displays a specific endpoint stored in the server.
    The endpoint information is printed in a json format for easy readability and further processing.
    If the endpoint is not available, an error message is printed.
    """,
)
def get(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Getting endpoint {endpoint_id} ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        deployment = client.get(model_id, version_id, endpoint_id)
    except ValidationError as e:
        echo.error("Endpoint validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error(f"⛔️Could not get endpoint {endpoint_id}")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(deployment.json())


@app.command(
    name="list-proofs",
    short_help="🔒 List proofs from an endpoint.",
    help="""🔒 List proofs from an endpoint.
    This command retrieves and displays the proofs generated by a specific endpoint stored in the server.
    The proofs' information is printed in a json format for easy readability and further processing.
    If the endpoint is not available, an error message is printed.
    """,
)
def list_proofs(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Getting proofs from endpoint {endpoint_id} ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        proofs: ProofList = client.list_proofs(model_id, version_id, endpoint_id)
    except ValidationError as e:
        echo.error("Could not retrieve proofs from endpoint")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error(f"⛔️Could not get endpoint {endpoint_id}")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(proofs.json(exclude_unset=True))


@app.command(
    name="get-proof",
    short_help="🔒 Retrieves information about a proof from an endpoint.",
    help="""🔒 Retrieves information about a proof from an endpoint.
    This command retrieves and displays the proof generated by a specific endpoint stored in the server.
    The proof information is printed in a json format for easy readability and further processing.
    If the endpoint is not available, an error message is printed.
    """,
)
def get_proof(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    proof_id: str = typer.Option(
        None, "--proof-id", "-p", help="The ID or request id of the proof"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Getting proof from endpoint {endpoint_id} ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        proof: Proof = client.get_proof(model_id, version_id, endpoint_id, proof_id)
    except ValidationError as e:
        echo.error("Could not retrieve proof from endpoint")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error(f"⛔️Could not get endpoint {endpoint_id}")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(proof.json(exclude_unset=True))


@app.command(
    name="download-proof",
    short_help="🔒 Downloads a proof from an endpoint to the specified path.",
    help="""🔒 Downloads a proof from an endpoint to the specified path.
    This command retrieves the proof created in Giza from a specific endpoint.
    The proof information is stored in the specified path, defaulting to the current path.
    If the endpoint is not available, an error message is printed.
    """,
)
def download_proof(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    proof_id: str = typer.Option(
        None, "--proof-id", "-p", help="The ID or request id of the proof"
    ),
    output_path: str = typer.Option(
        "zk.proof",
        "--output-path",
        "-o",
        help="The path where the proof will be stored",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Getting proof from endpoint {endpoint_id} ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        proof: bytes = client.download_proof(
            model_id, version_id, endpoint_id, proof_id
        )
        with open(output_path, "wb") as f:
            f.write(proof)
    except ValidationError as e:
        echo.error("Could not retrieve proof from endpoint")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error(f"⛔️Could not get endpoint {endpoint_id}")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    echo(f"Proof downloaded to {output_path} ✅ ")
