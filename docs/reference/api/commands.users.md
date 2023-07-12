<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.users`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create`

```python
create(
    debug: Optional[bool] = <typer.models.OptionInfo object at 0x104ce5050>
) → None
```

Command to create a user. Asks for the new users information and validates the input, then sends the information to the API



**Args:**

 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False).



**Raises:**

 - <b>`ValidationError`</b>:  input fields are validated, if these are not suitable the exception is raised
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `login`

```python
login(
    renew: bool = <typer.models.OptionInfo object at 0x104d1c850>,
    debug: Optional[bool] = <typer.models.OptionInfo object at 0x104ce5050>
) → None
```

Logs the current user to Giza Platform. Under the hood this will retrieve the token for the next requests. This token will be saved at `home` directory for further usage.



**Args:**

 - <b>`renew`</b> (bool):  Force the retrieval of the token to create a new one. Defaults to False.
 - <b>`debug`</b> (Optional[bool]):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False)



**Raises:**

 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `me`

```python
me(
    debug: Optional[bool] = <typer.models.OptionInfo object at 0x104ce5050>
) → None
```

Retrieve information about the current user and print it as json to stdout.



**Args:**

 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False)
