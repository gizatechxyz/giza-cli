import click
import typer
import typer.rich_utils
from rich.traceback import install

from giza.cli.commands.actions import app as actions_app
from giza.cli.commands.agents import app as agents_app
from giza.cli.commands.endpoints import app as deployments_app
from giza.cli.commands.endpoints import deploy
from giza.cli.commands.models import app as models_app
from giza.cli.commands.prove import prove
from giza.cli.commands.reset_password import (
    request_reset_password_token,
    reset_password,
)
from giza.cli.commands.users import app as users_app
from giza.cli.commands.verify import verify
from giza.cli.commands.version import check_version
from giza.cli.commands.versions import app as versions_app
from giza.cli.commands.versions import transpile
from giza.cli.commands.workspaces import app as workspaces_app
from giza.cli.utils import echo

install(suppress=[click])

app = typer.Typer(rich_markup_mode="markdown", pretty_exceptions_show_locals=False)
app.add_typer(
    users_app,
    name="users",
    short_help="💻 Utilities for managing users",
    help="""💻 Utilities for managing users""",
)

app.add_typer(
    agents_app,
    name="agents",
    short_help="💻 Utilities for managing agents",
    help="""💻 Utilities for managing agents""",
)

app.add_typer(
    models_app,
    name="models",
    short_help="💻 Utilities for managing models",
    help="""💻 Utilities for managing models""",
)

app.add_typer(
    workspaces_app,
    name="workspaces",
    short_help="💻 Utilities for managing workspaces",
    help="""💻 Utilities for managing workspaces""",
)

app.add_typer(
    deployments_app,
    name="deployments",
    short_help="🚀 Utilities for managing deployments (deprecated)",
    help="""🚀 Utilities for managing deployments (deprecated)""",
    callback=lambda: echo.warning(
        "The `deployments` command is deprecated and will be removed in the future. Use the `endpoints` command instead."
    ),
    deprecated=True,
)

app.add_typer(
    deployments_app,
    name="endpoints",
    short_help="🚀 Utilities for managing endpoints",
    help="""🚀 Utilities for managing endpoints""",
)

app.add_typer(
    actions_app,
    name="actions",
    short_help="🎯 Utilities for managing actions",
    help="""🎯 Utilities for managing actions""",
)


app.callback(
    name="giza",
    help="""
    🔶 Giza-CLI to manage the resources at Giza 🔶.
    """,
    invoke_without_command=True,
)(check_version)


app.add_typer(
    versions_app,
    name="versions",
    short_help="💻 Utilities for managing versions",
    help="""💻 Utilities for managing versions""",
)

app.command(
    name="transpile",
    short_help="🔧 Sends the specified model for transpilation. Shortcut for `giza versions transpile`",
    help="""🔧 Sends the specified model for transpilation. Shortcut for `giza versions transpile`

    This command has different behavior depending on the framework:

        * For Cairo, it will transpile the specified file and upload it to Giza.
        * For EZKL, it will create a version and perform the trusted setup, creating al the necessary files for it.

    This command performs several operations:

        * Creates a version for the specified model
        * Uploads the specified file
        * Updates the status to UPLOADED
        * Polls the version until the status is either FAILED or COMPLETED
        * If the status is COMPLETED, downloads the model to the specified path

    Error handling is also incorporated into this process.

    """,
)(transpile)

app.command(
    short_help="🚀 Creates an endpoint for the specified model version. Shortcut for `giza endpoints deploy`",
    help="""🚀 Creates a endpoint for the specified model version. Shortcut for `giza endpoints deploy`.

    This command will create an inference endpoint in Giza for the vailable frameworks.

    This command performs several operations:

        * Creates an endpoint for the specified version
        * Uploads the specified version file
        * Polls the version until the status is either FAILED or COMPLETED
        * If the status is COMPLETED, sends back the endpoint url to make inference requests

    Error handling is also incorporated into this process.
    """,
)(deploy)

app.command(
    name="prove",
    short_help="🔒 Command to generate a proof",
    help="""🔒 Command to generate a proof.

    Depending on the framework, this command will do different things:

        * For Cairo, it will generate a proof using a trace and a memory file in that order.
        * For EZKL, it will generate a proof using the provided input, all the trusted setup will be retrieve during the job.

    This command will create a job with the specified size, but the amount of jobs will be rate limited by the backend.

    This command will do a couple of things behind the scenes:

        * Create a Proving Job

        * Check the status of the job periodically

        * If the jobs status is `COMPLETED` then the proof has been created at Giza

        * Perform a request to the API to retrieve the proof metadata

        * Download the proof to the output path

    """,
)(prove)

app.command(
    name="verify",
    short_help="✔️ Command to verify a proof",
    help="""✔️ Command to verify a proof.

    Depending on the framework, this command will do different things:

        * For Cairo, it will verify the proof using the without the need of a trusted setup.
        * For EZKL, it will verify the proof using the trusted setup, retrieving all the neccessary information from the API.

    This command will create a job with the specified size, but the amount of jobs will be rate limited by the backend.

    This command will do a couple of things behind the scenes:

        * Create a Verifying Job

        * Check the status of the job periodically

        * If the jobs status is `COMPLETED` then the proof has been created at Giza

        * Perform a request to the API to retrieve the proof metadata

        * If the job its successfull the verification will be OK, otherwise it will fail

    """,
)(verify)

app.command(
    name="reset-password",
    short_help="🔑 Reset the password for a user using a reset token",
    help="""🔑 Reset the password for a user using a reset token.

    This command will prompt you to enter your reset token and new password. It will then send a request to the server to reset the password for the account associated with the provided reset token. If successful, the password will be reset to the new password.

    If an error occurs during the process, the command will display detailed error information, including the HTTP status code and error message. If the `debug` option is enabled, the command will also raise an exception.

    """,
)(reset_password)


app.command(
    name="request-reset-password-token",
    short_help="🔑 Request a reset token for a user",
    help="""🔑 Request a reset token for a user.

    This command will prompt you to enter your email. It will then send a request to the server to generate a reset token for the account associated with the provided email. If successful, the reset token will be sent to the email associated with the account.

    If an error occurs during the process, the command will display detailed error information, including the HTTP status code and error message. If the `debug` option is enabled, the command will also raise an exception.

    """,
)(request_reset_password_token)


def entrypoint():
    app()
