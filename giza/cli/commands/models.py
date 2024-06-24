import sys
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError

from giza.cli import API_HOST
from giza.cli.client import ModelsClient
from giza.cli.options import DEBUG_OPTION, DESCRIPTION_OPTION, JSON_OPTION, MODEL_OPTION
from giza.cli.schemas.models import ModelCreate
from giza.cli.utils import echo, get_response_info

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
    model_id: int = MODEL_OPTION,
    json: Optional[bool] = JSON_OPTION,
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
    if json:
        echo.set_log_file()
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
    echo.print_model(model)


@app.command(
    short_help="📜 List the available models.",
    help="""📜 Lists all the available models in Giza.

    This command retrieves and displays a list of all models stored in the server.
    Each model's information is printed in a json format for easy readability and further processing.

    If there are no models available, an empty list is printed.
    """,
)
def list(
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Command to list all models.

    Args:
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False).

    Raises:
        ValidationError: input fields are validated, if these are not suitable the exception is raised
        HTTPError: request error to the API, 4XX or 5XX
    """
    if json:
        echo.set_log_file()
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
    echo.print_model(models)


@app.command(
    short_help="📦 Creates a new model in Giza.",
    help="""📦 Creates a new model in Giza.

    This command needs model details to create a new model on the server.

    If the model creation fails, an error message is printed.
    """,
)
def create(
    name: str = typer.Option(
        ..., "--name", "-n", help="Name of the model to be created"
    ),
    description: str = DESCRIPTION_OPTION,
    json: Optional[bool] = JSON_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Command to create a model. Asks for the new model's information and validates the input,
    then sends the information to the API

    Args:
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False).

    Raises:
        ValidationError: input fields are validated, if these are not suitable the exception is raised
        HTTPError: request error to the API, 4XX or 5XX
    """
    if json:
        echo.set_log_file()
    if name is None or name == "":
        echo.error("Name is required")
        sys.exit(1)
    echo("Creating model ✅ ")
    try:
        client = ModelsClient(API_HOST)
        model = client.create(ModelCreate(name=name, description=description))
    except ValidationError as e:
        echo.error("Model validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not create model")
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
    echo.print_model(model)
