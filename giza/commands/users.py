import typer
from requests import HTTPError
from rich import print_json
from rich.prompt import Prompt

from giza import API_HOST
from giza.client import UsersClient
from giza.schemas import users
from giza.utils import echo

app = typer.Typer()


@app.command()
def create():
    user = Prompt.ask("Enter your username :sunglasses:")
    password = Prompt.ask("Enter your password 🥷 ", password=True)
    email = Prompt.ask("Enter your email 📧")
    echo("Creating user in Giza Platform ✅ ")
    user = users.UserCreate(username=user, password=password, email=email)
    client = UsersClient(API_HOST)
    client.create(user)
    echo("User created ✅. Check for a verification email 📧")


@app.command()
def login(
    renew: bool = typer.Option(False, help="Force the renewal of the JWT token"),
):
    user = Prompt.ask("Enter your username :sunglasses:")
    password = Prompt.ask("Enter your password 🥷 ", password=True)

    echo("Log into Giza Platform")
    client = UsersClient(API_HOST)
    try:
        client.retrieve_token(user, password, renew=renew)
    except HTTPError as e:
        echo("⛔️[red]Could not authorize the user[/red]⛔️")
        echo(f"⛔️[red]Status code ->[/red] {e.response.status_code}⛔️")
        echo(f"⛔️[red]Error message ->[/red] {e.response.json()}⛔️")
        raise e
    echo("Successfully logged into Giza Platform ✅ ")


@app.command()
def me():
    echo("Retrieving information about me!")
    client = UsersClient(API_HOST)
    user = client.me()

    print_json(user.json())
