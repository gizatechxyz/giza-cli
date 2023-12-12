import sys
import zipfile
from io import BytesIO
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError
from rich import print_json

from giza import API_HOST
from giza.client import VersionsClient
from giza.frameworks import cairo, ezkl
from giza.options import DEBUG_OPTION
from giza.schemas.versions import Version, VersionList
from giza.utils import echo, get_response_info
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
    model_desc: str = typer.Option(
        None, help="Description of the Model to create if model_id is not provided"
    ),
    framework: Framework = typer.Option(Framework.CAIRO, "--framework", "-f"),
    output_path: str = typer.Option(
        "cairo_model",
        "--output-path",
        "-o",
        help="The path where the cairo model will be saved",
    ),
    input_data: str = typer.Option(
        None,
        "--input-data",
        "-i",
        help="The input data to use for the transpilation",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if framework == Framework.CAIRO:
        cairo.transpile(
            model_path=model_path,
            model_id=model_id,
            desc=desc,
            model_desc=model_desc,
            output_path=output_path,
            debug=debug,
        )
    elif framework == Framework.EZKL:
        ezkl.setup(
            model_path=model_path,
            model_id=model_id,
            desc=desc,
            model_desc=model_desc,
            input_data=input_data,
            debug=debug,
        )
    else:
        raise typer.BadParameter(
            f"Framework {framework} is not supported, please use one of the following: {Framework.CAIRO}, {Framework.EZKL}"
        )


app.command(
    short_help="🔧 Sends the specified model for transpilation.",
    help="""🔧 Sends the specified model for transpilation.

    This command has different behavior depending on the framework:

        * For Cairo, it will transpile the specified file and upload it to Giza.
        * For EZKL, it will create a version and perform the trusted setup, creating al the necessary files for it.

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
    short_help="⚡️ Download the transpiled cairo model if available.",
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


@app.command(
    short_help="⚡️ Download the original ONNX model.",
    help="""⚡️ Download the original ONNX model.

    Verification and an active token is needed.
    """,
)
def download_original(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
    output_path: str = typer.Option(
        "model.onnx", "--output-path", "-o", help="Path to output the ONNX model"
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

        echo("ONNX model is ready, downloading! ✅")
        onnx_model = client.download_original(model_id, version.version)

        with open(output_path, "wb") as f:
            f.write(onnx_model)

        echo(f"ONNX model saved at: {output_path}")

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
