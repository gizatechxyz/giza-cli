import zipfile
from io import BytesIO

from giza import API_HOST
from giza.client import TranspileClient
from giza.utils import echo


def transpile(model_path, output_path):
    echo(f"Reading model from path: {model_path}")
    with open(model_path, "rb") as f:
        model = f.read()
    client = TranspileClient(API_HOST)
    echo("Sending model for transpilation")
    content = client.transpile(model)
    echo("Transpilation recieved!✅")
    try:
        zip_file = zipfile.ZipFile(BytesIO(content))
    except zipfile.BadZipFile as e:
        echo("Something went wrong with the transpiled file")
        echo(str(content))
        raise e

    zip_file.extractall(output_path)
    echo(f"Transpilation saved at: {output_path}")
