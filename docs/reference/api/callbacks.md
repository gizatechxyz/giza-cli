<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/callbacks.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `callbacks`





---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/callbacks.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `version_callback`

```python
version_callback(value: bool) → None
```

Prints the current version when `--version` flag is added to a call. 



**Args:**
 
 - <b>`value`</b> (bool):  represents if the flag has been added or not to the call. 



**Raises:**
 
 - <b>`Exit`</b>:  exit the CLI execution 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/callbacks.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `debug_callback`

```python
debug_callback(_, value: bool)
```

If a call adds the `--debug` flag debugging mode is activated for external requests and API Clients. 



**Args:**
 
 - <b>`_`</b> (_type_):  discarded value 
 - <b>`value`</b> (bool):  represents if the flag has been added to the call or not 



**Returns:**
 
 - <b>`bool`</b>:  pass the value back so it can be used in the clients 


