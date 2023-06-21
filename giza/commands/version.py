import typer

from giza.callbacks import version_callback


def version_entrypoint(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    ),  # noqa
):
    pass
