import sys
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError
from rich import print_json

from giza import API_HOST
from giza.client import ModelsClient
from giza.options import DEBUG_OPTION
from giza.utils import echo, get_response_info

app = typer.Typer()


@app.command(
    short_help="📦 Retrieves information about a model in Giza.",
    help="""📦 Retrieves information about a model in Giza.

    This commands needs a model id to retrieve data from the server.

    Until the verification is complete the user won't be able to log in nor user other CLI capabilities.

    If no model exists with the specified id an empty json is printed.
    """,
)
def get(
    model_id: int = typer.Argument(None),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Command to create a user. Asks for the new users information and validates the input,
    then sends the information to the API

    Args:
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False).

    Raises:
        ValidationError: input fields are validated, if these are not suitable the exception is raised
        HTTPError: request error to the API, 4XX or 5XX
    """
    echo("Retrieving model information ✅ ")
    try:
        client = ModelsClient(API_HOST)
        model = client.get(model_id)
    except ValidationError as e:
        echo.error("Model validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not retrieve model information")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(model.json())


@app.command(
    short_help="📜 List the available models.",
    help="""📜 List the available models.
    """,
)
def list(
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo("Listing models ✅ ")
    try:
        client = ModelsClient(API_HOST)
        models = client.list()
    except ValidationError as e:
        echo.error("Model validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not list models")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(models.json())
