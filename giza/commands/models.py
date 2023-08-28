import sys
import zipfile
from io import BytesIO
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError
from rich import print_json

from giza import API_HOST
from giza.client import ModelsClient
from giza.commands.transpile import transpile
from giza.options import DEBUG_OPTION
from giza.utils import echo, get_response_info
from giza.utils.enums import ModelStatus

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


app.command(
    short_help="🔧 Sends the specified model for transpilation.",
    help="""🔧 Sends the specified model for transpilation.

    We take the specified ONNX model and send it for transpilation at Giza 🔶.

    This command can be used multiple times with different models to transpile.
    For transpiling new versions of a model make sure to change the name as of now model names must be unique per user.

    This command will do a couple of things behind the scenes:

        * Create a Model entity

        * Upload the model

        * Update the status of the model

        * Poll the model until the status is either FAILED or COMPLETED

        * If COMPLETED the model is downloaded
    """,
)(transpile)


@app.command(
    short_help="⚡️ Download the transpiled cairo model if available",
    help="""⚡️ Download the transpiled cairo model if available.

    Download an unzip a transpiled model.

    Verification and an active token is needed.
    """,
)
def download(
    model_id: int,
    output_path: str = typer.Option(
        "cairo_model", "--output-path", "-o", help="Path to output the cairo model"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Retrieve information about the current user and print it as json to stdout.

    Args:
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False)
    """

    client = ModelsClient(API_HOST, debug=debug)
    model = client.get(model_id)

    if model.status == ModelStatus.COMPLETED:
        echo("Transpilation is ready, downloading! ✅")
        cairo_model = client.download(model.id)
        try:
            zip_file = zipfile.ZipFile(BytesIO(cairo_model))
        except zipfile.BadZipFile as zip_error:
            echo.error("Something went wrong with the transpiled file")
            echo.error(f"Error -> {zip_error.args[0]}")
            if debug:
                raise zip_error
            sys.exit(1)
        zip_file.extractall(output_path)
        echo(f"Transpilation saved at: {output_path}")
    else:
        echo.error(f"Model status is not completed {model.status}")
