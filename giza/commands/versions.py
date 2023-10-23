import sys
import time
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError
from rich import print_json
from rich.progress import Progress, SpinnerColumn, TextColumn

from giza import API_HOST
from giza.client import ModelsClient, VersionsClient
from giza.options import DEBUG_OPTION
from giza.schemas.models import ModelCreate
from giza.schemas.versions import Version, VersionCreate, VersionList, VersionUpdate
from giza.utils import Echo, echo, get_response_info
from giza.utils.enums import Framework, VersionStatus

app = typer.Typer()


@app.command(
    short_help="📦 Retrieves information about a version in Giza.",
    help="""📦 Retrieves information about a version in Giza.

    This commands needs a model id and version id to retrieve data from the server.

    If no version exists with the specified id an empty json is printed.
    """,
)
def get(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if any([model_id is None, version_id is None]):
        echo.error("⛔️Model ID and version ID are required⛔️")
        sys.exit(1)
    echo("Retrieving version information ✅ ")
    try:
        client = VersionsClient(API_HOST)
        version: Version = client.get(model_id, version_id)
    except ValidationError as e:
        echo.error("Version validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not retrieve version information")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(version.json())


def transpile(
    model_path: str = typer.Argument(None, help="Path of the model to transpile"),
    model_id: int = typer.Option(
        None, help="The ID of the model where a new version will be created"
    ),
    desc: str = typer.Option(None, help="Description of the version"),
    model_desc: int = typer.Option(
        None, help="Description of the Model to create if model_id is not provided"
    ),
    output_path: str = typer.Option(
        "cairo_model",
        "--output-path",
        "-o",
        help="The path where the cairo model will be saved",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    This function is responsible for transpiling a model. The overall objective is to prepare a model for use by converting it into a different format (transpiling).
    The function performs the following steps:

    1. Checks if a model_id is provided. If not, it extracts the model_name from the model_path.
    2. If a model description is provided and a model_id is also provided, it ignores the provided description.
    3. It then attempts to retrieve the model. If the model does not exist, it creates a new one.
    4. The function then creates a new version for the model, uploads the model file, and updates the status to UPLOADED.
    5. It then continuously checks the status of the version until it is either COMPLETED or FAILED.
    6. If the status is COMPLETED, it downloads the model to the specified path.
    7. If any errors occur during this process, they are handled and appropriate error messages are displayed.

    Args:
        model_path (str): Path of the model to transpile.
        model_id (int, optional): The ID of the model where a new version will be created. Defaults to None.
        desc (int, optional): Description of the version. Defaults to None.
        model_desc (int, optional): Description of the Model to create if model_id is not provided. Defaults to None.
        output_path (str, optional): The path where the cairo model will be saved. Defaults to "cairo_model".
        debug (bool, optional): A flag used to determine whether to raise exceptions or not. Defaults to DEBUG_OPTION.

    Raises:
        ValidationError: If there is a validation error with the model or version.
        HTTPError: If there is an HTTP error while communicating with the server.
    """
    echo = Echo(debug=debug)
    if model_id is None:
        model_name = model_path.split("/")[-1].split(".")[0]
        echo("No model id provided, checking if model exists ✅ ")
        echo(f"Model name is: {model_name}")
    if model_desc is not None and model_id is not None:
        echo(
            "Model description is not required when model id is provided, ignoring provided description ✅ "
        )
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            model_task = progress.add_task(
                description="Retrieving Model...", total=None
            )
            echo.debug(f"Reading model from path: {model_path}")
            models_client = ModelsClient(API_HOST)
            if model_id is None:
                model = models_client.get_by_name(model_name)
                if model is not None:
                    echo("Model already exists, using existing model ✅ ")
                else:
                    model_create = ModelCreate(name=model_name, description=model_desc)
                    model = models_client.create(model_create)
                    echo(f"Model Created with id -> {model.id}! ✅")
            else:
                model = models_client.get(model_id)
                echo(f"Model found with id -> {model.id}! ✅")
            progress.update(model_task, completed=True, visible=False)
            version_task = progress.add_task(
                description="Creating Version...", total=None
            )
            client = VersionsClient(API_HOST)
            version_create = VersionCreate(
                description=desc if desc else "Intial version",
                size=Path(model_path).stat().st_size,
                framework=Framework.CAIRO,
            )
            version, upload_url = client.create(
                model.id, version_create, model_path.split("/")[-1]
            )
            progress.update(version_task, completed=True, visible=False)
            echo("Sending model for transpilation ✅ ")
            with open(model_path, "rb") as f:
                client._upload(upload_url, f)
                echo.debug("Model Uploaded! ✅")

            client.update(
                model.id, version.version, VersionUpdate(status=VersionStatus.UPLOADED)
            )

            progress.add_task(description="Transpiling Model...", total=None)
            start_time = time.time()
            while True:
                version = client.get(model.id, version.version)
                if version.status not in (
                    VersionStatus.COMPLETED,
                    VersionStatus.FAILED,
                ):
                    spent = time.time() - start_time
                    echo.debug(
                        f"[{spent:.2f}s]Transpilation is not ready yet, retrying in 10s"
                    )
                    time.sleep(10)
                elif version.status == VersionStatus.COMPLETED:
                    echo.debug("Transpilation is ready, downloading! ✅")
                    cairo_model = client.download(model.id, version.version)
                    break
                elif version.status == VersionStatus.FAILED:
                    echo.error("⛔️ Transpilation failed! ⛔️")
                    echo.error(f"⛔️ Reason -> {version.message} ⛔️")
                    sys.exit(1)

    except ValidationError as e:
        echo.error("Version validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Error at transpilation⛔️")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)

    echo("Transpilation recieved! ✅")
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


app.command(
    short_help="🔧 Sends the specified model for transpilation.",
    help="""🔧 Sends the specified model for transpilation.

    This command performs several operations:

        * Creates a version for the specified model
        * Uploads the specified file
        * Updates the status to UPLOADED
        * Polls the version until the status is either FAILED or COMPLETED
        * If the status is COMPLETED, downloads the model to the specified path

    Error handling is also incorporated into this process.
    """,
)(transpile)


@app.command(
    short_help="🔄 Update the description of a version.",
    help="""🔄 Update the description of a version.

    This command needs a model id and version id to update the description of a version.
    """,
)
def update(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
    description: str = typer.Option(
        None, "--description", "-d", help="New description for the version"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if any([model_id is None, version_id is None, description is None]):
        echo.error(
            "⛔️Model ID, version ID and description are required to update the version⛔️"
        )
        sys.exit(1)
    echo("Updating version description ✅ ")
    try:
        client = VersionsClient(API_HOST)
        version = client.update(model_id, version_id, description)
    except ValidationError as e:
        echo.error("Version validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not update version")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(version.json())


@app.command(
    short_help="📜 List the available versions for a model.",
    help="""📜 List the available versions for a model.

    This command needs a model id to retrieve the list of versions.
    """,
)
def list(
    model_id: int = typer.Option(None, help="The ID of the model"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if model_id is None:
        echo.error("⛔️Model ID is required⛔️")
        sys.exit(1)
    echo("Listing versions for the model ✅ ")
    try:
        client = VersionsClient(API_HOST)
        versions: VersionList = client.list(model_id)
    except ValidationError as e:
        echo.error("Version validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not list versions for the model")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
    print_json(versions.json())


@app.command(
    short_help="⚡️ Download the transpiled cairo model if available",
    help="""⚡️ Download the transpiled cairo model if available.

    Download an unzip a transpiled model.

    Verification and an active token is needed.
    """,
)
def download(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
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

    try:
        if any([model_id is None, version_id is None]):
            raise ValueError("⛔️Model ID and version ID are required⛔️")

        client = VersionsClient(API_HOST, debug=debug)
        version = client.get(model_id, version_id)

        if version.status != VersionStatus.COMPLETED:
            raise ValueError(f"Model version status is not completed {version.status}")

        echo("Transpilation is ready, downloading! ✅")
        cairo_model = client.download(model_id, version.version)

        try:
            zip_file = zipfile.ZipFile(BytesIO(cairo_model))
        except zipfile.BadZipFile as zip_error:
            raise ValueError(
                "Something went wrong with the transpiled file", zip_error.args[0]
            ) from None

        zip_file.extractall(output_path)
        echo(f"Transpilation saved at: {output_path}")

    except ValueError as e:
        echo.error(e.args[0])
        if debug:
            raise e
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Error at download")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
