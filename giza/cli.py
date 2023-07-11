import click
import typer
import typer.rich_utils
from rich.traceback import install

from giza.commands.transpile import transpile
from giza.commands.users import app as users_app
from giza.commands.version import version_entrypoint

install(suppress=[click])

app = typer.Typer(rich_markup_mode="markdown", pretty_exceptions_show_locals=False)
app.add_typer(
    users_app,
    name="users",
    short_help="💻 Utilities for managing users",
    help="""💻 Utilities for managing users""",
)

app.callback(
    name="giza",
    help="""
    🔶 Giza-CLI to manage the resources at Giza Platform 🔶.
""",
)(version_entrypoint)


app.command(
    name="transpile",
    short_help="🔧 Sends the specified model for transpilation.",
    help="""🔧 Sends the specified model for transpilation.

    We take the specified ONNX model and send it for transpilation at Giza Platform 🔶

    This command can be used multiple times with different models to transpile.
    For transpiling new versions of a model make sure to change the name as of now model names must be unique per user.
    """,
)(transpile)


def entrypoint():
    app()
