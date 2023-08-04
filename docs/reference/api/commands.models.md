<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.models`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/models.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get`

```python
get(
    model_id: int = typer.Argument(None),
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Command to create a user. Asks for the new users information and validates the input, then sends the information to the API 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False). 



**Raises:**
 
 - <b>`ValidationError`</b>:  input fields are validated, if these are not suitable the exception is raised 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/models.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download`

```python
download(
    model_id: int,
    output_path: str = typer.Option(
        "cairo_model", "--output-path", "-o", help="Path to output the cairo model",
    ),
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Retrieve information about the current user and print it as json to stdout. 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False) 


