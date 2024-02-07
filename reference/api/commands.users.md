<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.users`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create`

```python
create(
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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `login`

```python
login(
    renew: bool = typer.Option(False, help="Force the renewal of the JWT token"),
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Logs the current user into Giza. Under the hood this will retrieve the token for the next requests. This token will be saved at `home` directory for further usage. 



**Args:**
 
 - <b>`renew`</b> (bool):  Force the retrieval of the token to create a new one. Defaults to False. 
 - <b>`debug`</b> (Optional[bool]):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False) 



**Raises:**
 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_api_key`

```python
create_api_key(
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Create an API key for your user. You need to be logged in to create an API key. The API Key will be saved at `home` directory for further usage. 



**Args:**
 
 - <b>`debug`</b> (Optional[bool]):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False) 



**Raises:**
 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `me`

```python
me(
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Retrieve information about the current user and print it as json to stdout. 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False) 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/users.py#L204"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `resend_email`

```python
resend_email(
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Command to resend verification email. Asks for the user's email and sends the request to the API 



**Args:**
 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False). 



**Raises:**
 
 - <b>`ValidationError`</b>:  input fields are validated, if these are not suitable the exception is raised 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


