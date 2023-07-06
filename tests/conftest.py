import logging

from typer.testing import CliRunner

from giza.cli import app


def invoke_cli_runner(*args, **kwargs):
    """
    Helper method to invoke the CliRunner while asserting that the exit code is actually 0.
    """
    expected_error = (
        kwargs.pop("expected_error") if "expected_error" in kwargs else None
    )
    res = CliRunner().invoke(app, *args, **kwargs)

    if res.exit_code != 0:
        if not expected_error:
            logging.error("Exception in the cli runner: %s" % res.exception)
            raise res.exception
        else:
            logging.info("Expected exception in the cli runner: %s" % res.exception)

    return res
