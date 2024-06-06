import datetime as dt
from typing import Optional, Union

import typer
from pydantic import BaseModel, RootModel
from rich import print as rich_print
from rich import reconfigure
from rich.console import Console
from rich.table import Table

reconfigure(soft_wrap=True)


class Echo:
    """
    Helper class to use when printing output of the CLI.

    Provides utilities to print different levels of the messages and provides formatting capabilities to each of the levels.
    """

    def __init__(self, debug: Optional[bool] = False) -> None:
        self._debug = debug

    def format_message(
        self, message: str, field: str = "giza", color: str = "orange3"
    ) -> str:
        """
        Format a message with an specific field and color.
        Adds current time, provided field and prints it with the specified color.

        Args:
            message (str): the message to format with the CLI
            field (str): Main field to format with the message. Defaults to "giza".
            color (str): Color to format the message with. Defaults to "orange3".

        Returns:
            str: the formatted message
        """
        formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_message = (
            rf"[{color}]\[{field}][/{color}][{formatted_time}] {message}"
        )
        return formatted_message

    def format_debug(self, message: str) -> str:
        """
        Specific format for debug purposes

        Args:
            message (str): message to format

        Returns:
            str: debug formatted message
        """
        return self.format_message(message, "giza-debug", "red")

    def format_error(self, message: str) -> str:
        """
        Specific format for error purposes

        Args:
            message (str): message to format

        Returns:
            str: error formatted message
        """
        return self.format_message(rf"[red]{message}[/red]", "ERROR", "red")

    def format_warning(self, message: str) -> str:
        """
        Specific format for warning purposes

        Args:
            message (str): message to format

        Returns:
            str: error formatted message
        """
        yellow = typer.colors.YELLOW
        return self.format_message(
            rf"[{yellow}]{message}[/{yellow}]", "WARN", f"{yellow}"
        )

    def echo(self, message: str, formatted: str) -> None:
        """
        Main function to print information of a message, original message is provided as well as the formatted one.
        Original is used when formatting is not possible.

        Args:
            message (str): original message
            formatted (str): formatted message
        """
        try:
            rich_print(formatted)
        except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError):
            # fallback to the standard print behaviour
            formatted_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            formatted_message = f"[giza][{formatted_time}] {message}"
            typer.echo(formatted_message)

    def error(self, message: str) -> None:
        """
        Format and echo an error message

        Args:
            message (str): error message to format and echo
        """
        formatted_message = self.format_error(message)
        self.echo(message, formatted_message)

    def debug(self, message: str) -> None:
        """
        Format and echo a debug message

        Args:
            message (str): debug message to format and echo
        """
        if self._debug:
            formatted_message = self.format_debug(message)
            self.echo(message, formatted_message)

    def info(self, message: str) -> None:
        """
        Format and echo a message

        Args:
            message (str): message to format and echo
        """
        formatted_message = self.format_message(message)
        self.echo(message, formatted_message)

    def warning(self, message: str) -> None:
        """
        Format and echo a warning message

        Args:
            message (str): message to format and echo
        """
        formatted_message = self.format_warning(message)
        self.echo(message, formatted_message)

    def __call__(self, message: str) -> None:
        """
        Provided as facility to echo through the class instance

        Args:
            message (str): message to formatt and print
        """
        self.info(message)

    def _extract_row(self, model: BaseModel) -> list:
        """
        Extracts the row from a model

        Args:
            model (BaseModel): A pydantic model which we extreact the fields value and set to "" if None

        Returns:
            list: A list with the values of the fields
        """
        result = []

        for field in model.model_fields.keys():
            value = getattr(model, field, "")
            if value is None:
                value = ""
            result.append(str(value))

        return result

    def print_model(self, model: Union[BaseModel, RootModel], title=""):
        """
        Utility function to print a model or a list of models in a table for pretty printing

        Args:
            model (Union[BaseModel, RootModel]): The model or list of models to print
            title (str, optional): Title of the table. Defaults to "".
        """

        table = Table(title=title)
        console = Console()

        # If its a root model we need to iterate over the root list and add a row for each model
        # RootModel goes first as it is a subclass of BaseModel
        if isinstance(model, RootModel):
            # We pick the first model to get the fields
            try:
                for field in model.root[0].model_fields.keys():
                    table.add_column(field, overflow="fold")
            except IndexError:
                return
            for m in model.root:
                table.add_row(*self._extract_row(m))
        # If its a single model we just create a table with the fields, one single row
        elif isinstance(model, BaseModel):
            for field in model.model_fields.keys():
                table.add_column(field)
            table.add_row(*self._extract_row(model))

        console.print(table)
