import sys
import zipfile
from io import BytesIO
from typing import Optional

from giza import API_HOST
from giza.client import TranspileClient
from giza.options import DEBUG_OPTION
from giza.utils import echo, echo_error


def transpile(
    model_path: str,
    output_path: str = "cairo_model",
    debug: Optional[bool] = DEBUG_OPTION,
):
    echo(f"Reading model from path: {model_path}")
    client = TranspileClient(API_HOST, debug=debug)
    echo("Sending model for transpilation")
    with open(model_path, "rb") as model:
        content = client.transpile(model)
    echo("Transpilation recieved! ✅")
    try:
        zip_file = zipfile.ZipFile(BytesIO(content))
    except zipfile.BadZipFile as e:
        echo_error("Something went wrong with the transpiled file")
        echo_error(str(content))
        if debug:
            raise e
        sys.exit(1)

    zip_file.extractall(output_path)
    echo(f"Transpilation saved at: {output_path}")
