import sys
from typing import Optional

import typer
from requests import HTTPError
from rich import print_json
from rich.prompt import Prompt

from giza import API_HOST
from giza.client import UsersClient
from giza.options import DEBUG_OPTION
from giza.schemas import users
from giza.utils import echo, echo_error, get_response_info

app = typer.Typer()


@app.command()
def create(debug: Optional[bool] = DEBUG_OPTION):
    user = Prompt.ask("Enter your username :sunglasses:")
    password = Prompt.ask("Enter your password 🥷 ", password=True)
    email = Prompt.ask("Enter your email 📧")
    echo("Creating user in Giza Platform ✅ ")
    user_create = users.UserCreate(username=user, password=password, email=email)
    client = UsersClient(API_HOST)
    client.create(user_create)
    echo("User created ✅. Check for a verification email 📧")


@app.command()
def login(
    renew: bool = typer.Option(False, help="Force the renewal of the JWT token"),
    debug: Optional[bool] = DEBUG_OPTION,
):
    user = Prompt.ask("Enter your username :sunglasses:")
    password = Prompt.ask("Enter your password 🥷 ", password=True)

    echo("Log into Giza Platform")
    client = UsersClient(API_HOST, debug=debug)
    try:
        client.retrieve_token(user, password, renew=renew)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo_error("⛔️Could not authorize the user⛔️")
        echo_error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo_error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo_error(f"⛔️Error message -> {info.get('content')}⛔️")
        if debug:
            raise e
        sys.exit(1)
    echo("Successfully logged into Giza Platform ✅ ")


@app.command()
def me(debug: Optional[bool] = DEBUG_OPTION):
    echo("Retrieving information about me!")
    client = UsersClient(API_HOST, debug=debug)
    user = client.me()

    print_json(user.json())
