import typer

from giza.cli.callbacks import debug_callback
from giza.cli.utils.enums import Framework

DEBUG_OPTION = typer.Option(
    False,
    "--debug",
    is_flag=True,
    callback=debug_callback,
    help="""
    Enable debugging of HTTP calls.


    Disabled by default.""",
)

MODEL_OPTION = typer.Option(None, "--model-id", "-m", help="The ID of the model")
VERSION_OPTION = typer.Option(None, "--version-id", "-v", help="The ID of the version")
ENDPOINT_OPTION = typer.Option(
    None, "--endpoint-id", "-e", help="The endpoint ID to use"
)
AGENT_OPTION = typer.Option(
    None,
    "--agent-id",
    "-a",
    help="The ID of the agent",
)
OUTPUT_PATH_OPTION = typer.Option(
    "cairo_model", "--output-path", "-o", help="The path to save the output to"
)
DESCRIPTION_OPTION = typer.Option(
    None, "--description", "-d", help="The description of the resource"
)
FRAMEWORK_OPTION = typer.Option(Framework.CAIRO, "--framework", "-f")
INPUT_OPTION = typer.Option(
    None,
    "--input-data",
    "-i",
    help="The input data to use",
)
NAME_OPTION = typer.Option(None, "--name", "-n", help="The name of the resource")
JSON_OPTION = typer.Option(
    False,
    "--json",
    "-j",
    help="Whether to print the output as JSON. This will make that the only ouput is the json and the logs will be saved to `giza.log`",
)
