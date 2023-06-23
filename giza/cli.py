import click
import typer
import typer.rich_utils
from rich.traceback import install

from giza.commands.transpile import transpile as transpile_entrypoint
from giza.commands.users import app as users_app
from giza.commands.version import version_entrypoint

install(suppress=[click])

app = typer.Typer(rich_markup_mode="markdown", pretty_exceptions_show_locals=False)
app.add_typer(users_app, name="users")

app.callback(
    name="giza",
    help="""
    🚀 Giza-CLI to manage the resources at Giza Platform 🚀.
""",
)(version_entrypoint)


@app.command()
def transpile(model_path: str, output_path: str = "cairo_model"):
    transpile_entrypoint(model_path, output_path)


def entrypoint():
    app()
