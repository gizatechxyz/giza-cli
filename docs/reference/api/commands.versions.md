<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.versions`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get`

```python
get(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `transpile`

```python
transpile(
    model_path: str = typer.Argument(None, help="Path of the model to transpile"),
    model_id: int = typer.Option(
        None, help="The ID of the model where a new version will be created"
    ),
    desc: str = typer.Option(None, help="Description of the version"),
    model_desc: int = typer.Option(
        None, help="Description of the Model to create if model_id is not provided"
    ),
    output_path: str = typer.Option(
        "cairo_model",
        "--output-path",
        "-o",
        help="The path where the cairo model will be saved",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```

This function is responsible for transpiling a model. The overall objective is to prepare a model for use by converting it into a different format (transpiling). The function performs the following steps: 

1. Checks if a model_id is provided. If not, it extracts the model_name from the model_path. 2. If a model description is provided and a model_id is also provided, it ignores the provided description. 3. It then attempts to retrieve the model. If the model does not exist, it creates a new one. 4. The function then creates a new version for the model, uploads the model file, and updates the status to UPLOADED. 5. It then continuously checks the status of the version until it is either COMPLETED or FAILED. 6. If the status is COMPLETED, it downloads the model to the specified path. 7. If any errors occur during this process, they are handled and appropriate error messages are displayed. 



**Args:**
 
 - <b>`model_path`</b> (str):  Path of the model to transpile. 
 - <b>`model_id`</b> (int, optional):  The ID of the model where a new version will be created. Defaults to None. 
 - <b>`desc`</b> (int, optional):  Description of the version. Defaults to None. 
 - <b>`model_desc`</b> (int, optional):  Description of the Model to create if model_id is not provided. Defaults to None. 
 - <b>`output_path`</b> (str, optional):  The path where the cairo model will be saved. Defaults to "cairo_model". 
 - <b>`debug`</b> (bool, optional):  A flag used to determine whether to raise exceptions or not. Defaults to DEBUG_OPTION. 



**Raises:**
 
 - <b>`ValidationError`</b>:  If there is a validation error with the model or version. 
 - <b>`HTTPError`</b>:  If there is an HTTP error while communicating with the server. 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L235"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update`

```python
update(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
    description: str = typer.Option(
        None, "--description", "-d", help="New description for the version"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L281"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `list`

```python
list(
    model_id: int = typer.Option(None, help="The ID of the model"),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download`

```python
download(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
    output_path: str = typer.Option(
        "cairo_model", "--output-path", "-o", help="Path to output the cairo model"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```

Retrieve information about the current user and print it as json to stdout. 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False) 


