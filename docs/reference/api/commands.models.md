<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.models`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/models.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get`

```python
get(
    model_id: int = typer.Option(
        ..., "--model-id", "-m", help="Model id to retrieve information from"
    ),
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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/models.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `list`

```python
list(
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Command to list all models. 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False). 



**Raises:**
 
 - <b>`ValidationError`</b>:  input fields are validated, if these are not suitable the exception is raised 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/models.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create`

```python
create(
    name: str = typer.Option(
        ..., "--name", "-n", help="Name of the model to be created"
    ),
    description: str = typer.Option(
        None, "--description", "-d", help="Description of the model to be created"
    ),
    debug: Optional[bool] = **DEBUG_OPTION**
) → None
```

Command to create a model. Asks for the new model's information and validates the input, then sends the information to the API 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False). 



**Raises:**
 
 - <b>`ValidationError`</b>:  input fields are validated, if these are not suitable the exception is raised 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


