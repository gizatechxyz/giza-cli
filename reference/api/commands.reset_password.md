<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/reset_password.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.reset_password`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/reset_password.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prompt_for_input`

```python
prompt_for_input(
    prompt_message: str,
    type: Optional[type] = <class 'str'>,
    hide_input: bool = False
) → str
```

Prompt the user for input. 



**Args:**
 
 - <b>`prompt_message`</b> (str):  The message to display when prompting the user. 
 - <b>`type`</b> (type, optional):  The type of input to expect. Defaults to str. 
 - <b>`hide_input`</b> (bool, optional):  Whether to hide the input (for passwords). Defaults to False. 



**Returns:**
 
 - <b>`str`</b>:  The user's input. 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/reset_password.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `handle_http_error`

```python
handle_http_error(
    e: HTTPError,
    error_msg: str,
    debug: Optional[bool] = DEBUG_OPTION
) → None
```

Handle an HTTP error. 



**Args:**
 
 - <b>`e`</b> (HTTPError):  The error to handle. 
 - <b>`debug`</b> (Optional[bool]):  Whether to raise the error for debugging. Defaults to DEBUG_OPTION. 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/reset_password.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `request_reset_password_token`

```python
request_reset_password_token(
    email: str = typer.Option(None, "--email"),
    debug: Optional[bool] = DEBUG_OPTION
) → bool
```

Request a password reset token for a given email. 



**Args:**
 
 - <b>`email`</b> (str):  The email to request a password reset for. 
 - <b>`debug`</b> (Optional[bool]):  Whether to raise errors for debugging. Defaults to DEBUG_OPTION. 



**Returns:**
 
 - <b>`bool`</b>:  True if the request was successful, False if not. 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/reset_password.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `reset_password`

```python
reset_password(
    token: str = typer.Option(None, "--token"),
    debug: Optional[bool] = DEBUG_OPTION
) → bool
```

Reset the password for a user using a reset token. 



**Args:**
 
 - <b>`token`</b> (str):  The reset token received by email. 
 - <b>`debug`</b> (Optional[bool]):  Whether to raise errors for debugging. Defaults to DEBUG_OPTION. 



**Returns:**
 
 - <b>`bool`</b>:  True if the reset was successful, False if not. 


