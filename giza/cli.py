import click
import typer
import typer.rich_utils
from rich.traceback import install

from giza.commands.models import app as models_app
from giza.commands.prove import prove
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

app.add_typer(
    models_app,
    name="models",
    short_help="💻 Utilities for managing models",
    help="""💻 Utilities for managing models""",
)

app.callback(
    name="giza",
    help="""
    🔶 Giza-CLI to manage the resources at Giza 🔶.
""",
)(version_entrypoint)


app.command(
    name="transpile",
    short_help="🔧 Sends the specified model for transpilation. Shortcut for `giza models transpile`.",
    help="""🔧 Sends the specified model for transpilation. Shortcut for `giza models transpile`.

    We take the specified ONNX model and send it for transpilation at Giza 🔶.

    This command can be used multiple times with different models to transpile.
    For transpiling new versions of a model make sure to change the name as of now model names must be unique per user.

    This command will do a couple of things behind the scenes:

        * Create a Model entity

        * Upload the model

        * Update the status of the model

        * Poll the model until the status is either FAILED or COMPLETED

        * If COMPLETED the model is downloaded

    """,
)(transpile)

app.command(name="prove")(prove)


def entrypoint():
    app()
