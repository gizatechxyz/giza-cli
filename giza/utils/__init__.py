import datetime as dt
from typing import Any

import typer
from rich import print as rich_print
from rich import reconfigure

reconfigure(soft_wrap=True)


def format_message(message: Any) -> str:
    formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    formatted_message = rf"[orange3]\[giza][/orange3][{formatted_time}] {message}"
    return formatted_message


def echo(message: Any):
    formatted_message = format_message(message)
    try:
        rich_print(formatted_message)
    except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError):
        # fallback to the standard print behaviour
        formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_message = f"[giza][{formatted_time}] {message}"
        typer.echo(formatted_message)
