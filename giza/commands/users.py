import typer
from rich.prompt import Prompt

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
    echo("User created ✅. Check for a verification email 📧")


@app.command()
def verify(token: str):
    print("verify")


@app.command()
def me():
    print("me")
