import datetime as dt
import json
from typing import Any

import typer
from requests import Response
from rich import print as rich_print
from rich import reconfigure

reconfigure(soft_wrap=True)


def format_message(message: Any) -> str:
    formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    formatted_message = rf"[orange3]\[giza][/orange3][{formatted_time}] {message}"
    return formatted_message


def format_debug_message(message: Any) -> str:
    formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    formatted_message = rf"[red]\[giza-debug][/red][{formatted_time}] {message}"
    return formatted_message


def format_error_message(message: Any) -> str:
    formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    formatted_message = rf"[red]\[ERROR][/red][{formatted_time}] [red]{message}[/red]"
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


def echo_error(message: Any):
    formatted_message = format_error_message(message)
    try:
        rich_print(formatted_message)
    except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError):
        # fallback to the standard print behaviour
        formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_message = f"[giza][{formatted_time}] {message}"
        typer.echo(formatted_message)


def echo_debug(message: Any):
    formatted_message = format_debug_message(message)
    try:
        rich_print(formatted_message)
    except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError):
        # fallback to the standard print behaviour
        formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_message = f"[giza][{formatted_time}] {message}"
        typer.echo(formatted_message)


def get_response_info(response: Response):
    try:
        content = response.json()
        detail = content.get("detail")
    except json.JSONDecodeError:
        content = response.text if len(response.text) < 255 else response.text[:255]

    return {"content": content, "detail": detail, "status_code": response.status_code}
