import sys
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError

from giza.cli import API_HOST
from giza.cli.client import EndpointsClient
from giza.cli.frameworks import cairo, ezkl
from giza.cli.options import (
    DEBUG_OPTION,
    ENDPOINT_OPTION,
    FRAMEWORK_OPTION,
    JSON_OPTION,
    MODEL_OPTION,
    VERSION_OPTION,
)
from giza.cli.schemas.endpoints import EndpointsList
from giza.cli.schemas.proofs import Proof, ProofList
from giza.cli.utils import echo, get_response_info
from giza.cli.utils.enums import Framework, ServiceSize
from giza.cli.utils.exception_handling import ExceptionHandler

app = typer.Typer()


def deploy(
    data: str = typer.Argument(None),
    model_id: int = MODEL_OPTION,
    version_id: int = VERSION_OPTION,
    size: ServiceSize = typer.Option(ServiceSize.S, "--size", "-s"),
    framework: Framework = FRAMEWORK_OPTION,
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
    model_id: int = MODEL_OPTION,
    version_id: int = VERSION_OPTION,
    only_active: bool = typer.Option(
        False, "--only-active", "-a", help="Only list active endpoints"
    ),
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if json:
        echo.set_log_file()
    echo("Listing endpoints ✅ ")
    params = {}
    try:
        client = EndpointsClient(API_HOST)
        if model_id:
            params["model_id"] = model_id
        if version_id:
            params["version_id"] = version_id
        if only_active:
            params["is_active"] = True
        deployments: EndpointsList = client.list(params=params)
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
        (
            echo.error(
                f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
            )
            if info.get("request_id")
            else None
        )
        if debug:
            raise e
        sys.exit(1)
    echo.print_model(deployments)


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
    endpoint_id: int = ENDPOINT_OPTION,
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if json:
        echo.set_log_file()
    echo(f"Getting endpoint {endpoint_id} ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        deployment = client.get(endpoint_id)
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
        (
            echo.error(
                f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
            )
            if info.get("request_id")
            else None
        )
        if debug:
            raise e
        sys.exit(1)
    echo.print_model(deployment)


@app.command(
    name="delete",
    short_help="📡 Deletes an endpoint.",
    help="""📡 Deletes an endpoint and marks it as inactive.

    This command will remove the `endpoint` service but it will mark it as `inactive` so underlying resources are not deleted.

    Information about the inactives endpoint can be retrieved as well as the active ones.
    """,
)
def delete_endpoint(
    endpoint_id: int = ENDPOINT_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Deleting endpoint {endpoint_id} ✅ ")
    with ExceptionHandler(debug=debug):
        client = EndpointsClient(API_HOST)
        client.delete(endpoint_id)
    echo(f"Endpoint {endpoint_id} deleted ✅ ")


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
    endpoint_id: int = ENDPOINT_OPTION,
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if json:
        echo.set_log_file()
    echo(f"Getting proofs from endpoint {endpoint_id} ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        proofs: ProofList = client.list_proofs(endpoint_id)
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
        (
            echo.error(
                f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
            )
            if info.get("request_id")
            else None
        )
        if debug:
            raise e
        sys.exit(1)
    echo.print_model(proofs)


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
    endpoint_id: int = ENDPOINT_OPTION,
    proof_id: str = typer.Option(
        None, "--proof-id", "-p", help="The ID or request id of the proof"
    ),
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if json:
        echo.set_log_file()
    echo(f"Getting proof from endpoint {endpoint_id} ✅ ")
    try:
        client = EndpointsClient(API_HOST)
        proof: Proof = client.get_proof(endpoint_id, proof_id)
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
        (
            echo.error(
                f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
            )
            if info.get("request_id")
            else None
        )
        if debug:
            raise e
        sys.exit(1)
    echo.print_model(proof)


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
    endpoint_id: int = ENDPOINT_OPTION,
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
        proof: bytes = client.download_proof(endpoint_id, proof_id)
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
        (
            echo.error(
                f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
            )
            if info.get("request_id")
            else None
        )
        if debug:
            raise e
        sys.exit(1)
    echo(f"Proof downloaded to {output_path} ✅ ")


@app.command(
    name="list-jobs",
    short_help="💼 List jobs from an endpoint.",
    help="""💼 List jobs from an endpoint.
    This command retrieves and displays the jobs created by a specific endpoint to generate a proof of a request.
    The jobs information is printed in a json format for easy readability and further processing.
    If the endpoint is not available, an error message is printed.
    """,
)
def list_jobs(
    endpoint_id: int = ENDPOINT_OPTION,
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if json:
        echo.set_log_file()
    echo(f"Getting jobs from endpoint {endpoint_id} ✅ ")
    with ExceptionHandler(debug=debug):
        client = EndpointsClient(API_HOST)
        jobs = client.list_jobs(endpoint_id)
    echo.print_model(jobs)


@app.command(
    name="verify",
    short_help="🔍 Verify a proof from an endpoint.",
    help="""🔍 Verify a proof from an endpoint.
    This command verifies a proof generated by a specific endpoint.
    The verify information is printed in a json format for easy readability and further processing.
    If the endpoint is not available, an error message is printed.
    """,
)
def verify(
    endpoint_id: int = ENDPOINT_OPTION,
    proof_id: str = typer.Option(
        None, "--proof-id", "-p", help="The ID or request id of the proof"
    ),
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if json:
        echo.set_log_file()
    echo(f"Verifying proof from endpoint {endpoint_id} ✅ ")
    with ExceptionHandler(debug=debug):
        client = EndpointsClient(API_HOST)
        verification = client.verify_proof(endpoint_id, proof_id)
    echo.print_model(verification)


@app.command(
    short_help="📜 Retrieves the logs from a version",
    help="""📜 Retrieves the logs from a version

    This command will print the latest logs from the endpoint to help debug and understand
    what its happening under the hood.

    If no logs are available, an empty string is printed.
    """,
)
def logs(
    endpoint_id: int = ENDPOINT_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo(f"Getting logs for endpoint {endpoint_id} ✅ ")
    with ExceptionHandler(debug=debug):
        client = EndpointsClient(API_HOST)
        logs = client.get_logs(endpoint_id)
        if logs.logs == "":
            echo.warning("No logs available")
        else:
            print(logs.logs)
