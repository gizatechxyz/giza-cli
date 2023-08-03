<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.echo`






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Echo`
Helper class to use when printin output of the CLI.

Provides utilities to print different levels of the messages and provides formatting capabilities to each of the levels.

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(debug: bool = False) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `debug`

```python
debug(message: str) → None
```

Format and echo a debug message



**Args:**

 - <b>`message`</b> (str):  debug message to format and echo

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `echo`

```python
echo(message: str, formatted: str) → None
```

Main function to print information of a message, original message is provided as well as the formatted one. Original is used when formatting is not possible.



**Args:**

 - <b>`message`</b> (str):  original message
 - <b>`formatted`</b> (str):  formatted message

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `error`

```python
error(message: str) → None
```

Format and echo a error message



**Args:**

 - <b>`message`</b> (str):  error message to format and echo

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `format_debug`

```python
format_debug(message: str) → str
```

Specific format for debug purposes



**Args:**

 - <b>`message`</b> (str):  message to format



**Returns:**

 - <b>`str`</b>:  debug formatted message

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `format_error`

```python
format_error(message: str) → str
```

Specific format for error purposes



**Args:**

 - <b>`message`</b> (str):  message to format



**Returns:**

 - <b>`str`</b>:  error formatted message

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `format_message`

```python
format_message(message: str, field: str = 'giza', color: str = 'orange3') → str
```

Format a message with an specific field and color. Adds current time, provided field and prints it with the specified color.



**Args:**

 - <b>`message`</b> (str):  the message to format with the CLI
 - <b>`field`</b> (str):  Main field to format with the message. Defaults to "giza".
 - <b>`color`</b> (str):  Color to format the message with. Defaults to "orange3".



**Returns:**

 - <b>`str`</b>:  the formatted message

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/echo.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `info`

```python
info(message: str) → None
```

Format and echo a message



**Args:**

 - <b>`message`</b> (str):  message to format and echo
