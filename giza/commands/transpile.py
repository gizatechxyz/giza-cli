import sys
import time
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Optional

import typer
from requests import HTTPError
from rich import print_json
from rich.progress import Progress, SpinnerColumn, TextColumn

from giza import API_HOST
from giza.client import ModelsClient
from giza.options import DEBUG_OPTION
from giza.schemas.models import ModelCreate, ModelUpdate
from giza.utils import Echo, get_response_info
from giza.utils.enums import ModelStatus


def transpile(
    model_path: str = typer.Argument(None, help="Path of the model to transpile"),
    output_path: str = typer.Option(
        "cairo_model", "--output-path", "-o", help="Path to output the cairo model"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Command to transpile the model using the client. Sends the model and then unzips it to the desired location.

    This command will do a couple of things behind the scenes:
        * Create a Model entity
        * Upload the model
        * Update the status of the model
        * Poll the model until the status is either FAILED or COMPLETED
        * If COMPLETED the model is downloaded

    Args:
        model_path (str): path for the model to load
        output_path (str): ouput to store the transpiled model. Defaults to "cairo_model".
        debug (Optional[bool], optional): Whether to add debug information, will show requests,
            extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION(False).

    Raises:
        BadZipFile: if the recieved file is not a zip, could be due to a transpilation error at the API.
        HTTPError: request error to the API, 4XX or 5XX
    """
    echo = Echo(debug=debug)
    echo.debug(f"Reading model from path: {model_path}")
    client = ModelsClient(API_HOST, debug=debug)
    echo("Sending model for transpilation")

    model_create = ModelCreate(
        name=model_path.split("/")[-1], size=Path(model_path).stat().st_size
    )

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Uploading Model...", total=None)

            model, url = client.create(model_create)
            echo(f"Model Created with id -> {model.id}! ✅")
            if debug:
                print_json(model.json())

            with open(model_path, "rb") as f:
                client._upload(url, f)
            echo.debug("Model Uploaded! ✅")

            updated_model = client.update(
                model.id, ModelUpdate(status=ModelStatus.UPLOADED)
            )
            echo.debug(f"Model Status updated to: {updated_model.status}! ✅")

            progress.add_task(description="Transpiling Model...", total=None)
            start_time = time.time()
            while True:
                m = client.get(model.id)
                if m.status not in (ModelStatus.COMPLETED, ModelStatus.FAILED):
                    spent = time.time() - start_time
                    echo.debug(
                        f"[{spent:.2f}s]Transpilation is not ready yet, retrying in 10s"
                    )
                    time.sleep(10)
                elif m.status == ModelStatus.COMPLETED:
                    echo.debug("Transpilation is ready, downloading! ✅")
                    cairo_model = client.download(model.id)
                    break
                elif m.status == ModelStatus.FAILED:
                    echo.error("⛔️ Transpilation failed! ⛔️")
                    echo.error(f"⛔️ Reason -> {m.message} ⛔️")
                    break
    except HTTPError as http_error:
        info = get_response_info(http_error.response)
        echo.error("Error at transpilation")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise http_error
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
