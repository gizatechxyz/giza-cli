import sys
from typing import Optional

import typer
from pydantic import EmailStr, SecretStr, ValidationError
from requests import HTTPError
from rich import print_json
from rich.prompt import Prompt

from giza import API_HOST
from giza.client import UsersClient
from giza.options import DEBUG_OPTION
from giza.schemas import users
from giza.utils import echo, get_response_info

app = typer.Typer()


@app.command(
    short_help="🔥 Creates a new user in Giza.",
    help="""🔥 Creates a new user in Giza.

    This commands ask for a username, password and a valid email address,
    then a confirmation email will be sent to the provided one.

    Until the verification is complete the user won't be able to log in nor user other CLI capabilities.

    If a username or email is already registered and error will be raised.
    """,
)
def create(debug: Optional[bool] = DEBUG_OPTION) -> None:
    """
    Command to create a user. Asks for the new users information and validates the input,
    then sends the information to the API

    Args:
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False).

    Raises:
        ValidationError: input fields are validated, if these are not suitable the exception is raised
        HTTPError: request error to the API, 4XX or 5XX
    """
    user = Prompt.ask("Enter your username :sunglasses:")
    password = Prompt.ask("Enter your password 🥷 ", password=True)
    email = Prompt.ask("Enter your email 📧")
    echo("Creating user in Giza ✅ ")
    try:
        user_create = users.UserCreate(
            username=user, password=SecretStr(password), email=EmailStr(email)
        )
        client = UsersClient(API_HOST)
        client.create(user_create)
    except ValidationError as e:
        echo.error("⛔️Could not create the user⛔️")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not create the user⛔️")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        if debug:
            raise e
        sys.exit(1)
    echo("User created ✅. Check for a verification email 📧")


@app.command(
    short_help="🔶 Log into Giza.",
    help="""🔶 Log into Giza.

    Log into Giza using the provided credentials. This will retrieve a JWT
    that will be used to authenticate the user.

    This will be saved at `~/.giza/.credentials.json` for later re-use until the token expires.

    Verification is needed to log in.
    """,
)
def login(
    renew: bool = typer.Option(False, help="Force the renewal of the JWT token"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Logs the current user into Giza. Under the hood this will retrieve the token for the next requests.
    This token will be saved at `home` directory for further usage.

    Args:
        renew (bool): Force the retrieval of the token to create a new one. Defaults to False.
        debug (Optional[bool]): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False)

    Raises:
        HTTPError: request error to the API, 4XX or 5XX
    """
    user = Prompt.ask("Enter your username :sunglasses:")
    password = Prompt.ask("Enter your password 🥷 ", password=True)

    echo("Log into Giza")
    client = UsersClient(API_HOST, debug=debug)
    try:
        client.retrieve_token(user, password, renew=renew)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not authorize the user⛔️")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        if debug:
            raise e
        sys.exit(1)
    echo("Successfully logged into Giza ✅ ")


@app.command(
    short_help="💻 Retrieve information about the current user",
    help="""💻 Retrieve information about the current user.

    Makes an API call to retrieve user current information from Giza.

    Verification and an active token is needed.
    """,
)
def me(debug: Optional[bool] = DEBUG_OPTION) -> None:
    """
    Retrieve information about the current user and print it as json to stdout.

    Args:
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False)
    """
    echo("Retrieving information about me!")
    client = UsersClient(API_HOST, debug=debug)
    user = client.me()

    print_json(user.json())
