import sys
import zipfile
from io import BytesIO
from typing import Optional

from requests import HTTPError

from giza import API_HOST
from giza.client import TranspileClient
from giza.options import DEBUG_OPTION
from giza.utils import echo, get_response_info


def transpile(
    model_path: str,
    output_path: str = "cairo_model",
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Command to transpile the model using the client. Sends the model and then unzips it to the desired location.

    Args:
        model_path (str): path for the model to load
        output_path (str): ouput to store the transpiled model. Defaults to "cairo_model".
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION(False).

    Raises:
        BadZipFile: if the recieved file is not a zip, could be due to a transpilation error at the API.
        HTTPError: request error to the API, 4XX or 5XX
    """
    echo(f"Reading model from path: {model_path}")
    client = TranspileClient(API_HOST, debug=debug)
    echo("Sending model for transpilation")

    try:
        with open(model_path, "rb") as model:
            response = client.transpile(model)
    except HTTPError as http_error:
        info = get_response_info(http_error.response)
        echo.error("Error at transpilation")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        if debug:
            raise http_error
        sys.exit(1)
    echo("Transpilation recieved! ✅")
    try:
        zip_file = zipfile.ZipFile(BytesIO(response.content))
    except zipfile.BadZipFile as zip_error:
        echo.error("Something went wrong with the transpiled file")
        echo.error(f"Error -> {zip_error.args[0]}")
        if debug:
            raise zip_error
        sys.exit(1)

    zip_file.extractall(output_path)
    echo(f"Transpilation saved at: {output_path}")
