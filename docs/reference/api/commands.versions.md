<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.versions`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_sierra`

```python
update_sierra(model_id: int, version_id: int, model_path: str)
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get`

```python
get(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version"),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    framework: Framework = typer.Option(Framework.CAIRO, "--framework", "-f"),
    output_path: str = typer.Option(
        "cairo_model",
        "--output-path",
        "-o",
        help="The path where the cairo model will be saved",
    ),
    input_data: str = typer.Option(
        None,
        "--input-data",
        "-i",
        help="The input data to use for the transpilation",
    ),
    debug: Optional[bool] = DEBUG_OPTION
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L139"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `list`

```python
list(
    model_id: int = typer.Option(None, help="The ID of the model"),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download`

```python
download(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version")
    output_path: str = typer.Option(
        "cairo_model", "--output-path", "-o", help="Path to output the cairo model"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```

Retrieve information about the current user and print it as json to stdout. 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False) 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/versions.py#L269"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_original`

```python
download_original(
    model_id: int = typer.Option(None, help="The ID of the model"),
    version_id: int = typer.Option(None, help="The ID of the version")
    output_path: str = typer.Option(
        "cairo_model", "--output-path", "-o", help="Path to output the cairo model"
    ),
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Retrieve information about the current user and print it as json to stdout. 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False) 


