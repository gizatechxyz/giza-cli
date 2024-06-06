from typing import Union

from pydantic import BaseModel, RootModel
from rich.console import Console
from rich.table import Table


def extract_row(model: BaseModel) -> list:
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


def print_model(model: Union[BaseModel, RootModel], title=""):
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
                table.add_column(field)
        except IndexError:
            return
        for m in model.root:
            table.add_row(*extract_row(m))
    # If its a single model we just create a table with the fields, one single row
    elif isinstance(model, BaseModel):
        for field in model.model_fields.keys():
            table.add_column(field)
        table.add_row(*extract_row(model))

    console.print(table)
