from http import client

import typer

from giza import __version__
from giza.utils import echo


def version_callback(value: bool):
    if value:
        echo(
            f"🚀 [orange3]Giza[/orange3] Platform CLI, "
            f"version ~> [green]{__version__}[/green]",
        )
        raise typer.Exit()


def debug_callback(_, value: bool):
    if value:
        echo(":bug: Debugging mode is [red]on[/red]")
        client.HTTPConnection.debuglevel = 1

    return value
