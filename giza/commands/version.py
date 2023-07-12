import typer

from giza.callbacks import version_callback


def version_entrypoint(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    ),  # noqa
) -> None:
    """
    Prints the current CLI version.

    Args:
        version (bool): Tper callback to retrieve the version.
    """
    pass
