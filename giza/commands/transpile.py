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
):
    echo(f"Reading model from path: {model_path}")
    client = TranspileClient(API_HOST, debug=debug)
    echo("Sending model for transpilation")

    try:
        with open(model_path, "rb") as model:
            response = client.transpile(model)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("Error at transpilation")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        if debug:
            raise e
        sys.exit(1)
    echo("Transpilation recieved! ✅")
    try:
        zip_file = zipfile.ZipFile(BytesIO(response.content))
    except zipfile.BadZipFile as e:
        echo.error("Something went wrong with the transpiled file")
        echo.error(f"Error -> {e.args[0]}")
        if debug:
            raise e
        sys.exit(1)

    zip_file.extractall(output_path)
    echo(f"Transpilation saved at: {output_path}")
