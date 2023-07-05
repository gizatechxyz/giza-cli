import datetime as dt
from typing import Any

import typer
from rich import print as rich_print
from rich import reconfigure

reconfigure(soft_wrap=True)


class Echo:
    def format_message(
        self, message: Any, field: str = "giza", color: str = "orange3"
    ) -> str:
        formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_message = (
            rf"[{color}]\[{field}][/{color}][{formatted_time}] {message}"
        )
        return formatted_message

    def format_debug(self, message: Any) -> str:
        return self.format_message(message, "giza-debug", "red")

    def format_error(self, message: Any) -> str:
        return self.format_message(rf"[red]{message}[/red]", "ERROR", "red")

    def echo(self, message: Any, formatted: str):
        try:
            rich_print(formatted)
        except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError):
            # fallback to the standard print behaviour
            formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            formatted_message = f"[giza][{formatted_time}] {message}"
            typer.echo(formatted_message)

    def error(self, message: Any):
        formatted_message = self.format_error(message)
        self.echo(message, formatted_message)

    def debug(self, message: Any):
        formatted_message = self.format_debug(message)
        self.echo(message, formatted_message)

    def info(self, message: Any):
        formatted_message = self.format_message(message)
        self.echo(message, formatted_message)

    def __call__(self, message):
        self.info(message)
