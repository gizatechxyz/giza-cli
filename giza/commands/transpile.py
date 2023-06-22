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
    with open(output_path, "wb") as f:
        f.write(content)
    echo(f"Trasnpilation saved at: {output_path}")
