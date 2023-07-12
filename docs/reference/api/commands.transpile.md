<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/transpile.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.transpile`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/transpile.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `transpile`

```python
transpile(
    model_path: str,
    output_path: str = 'cairo_model',
    debug: Optional[bool] = <typer.models.OptionInfo object at 0x104ce5050>
) → None
```

Command to transpile the model using the client. Sends the model and then unzips it to the desired location.



**Args:**

 - <b>`model_path`</b> (str):  path for the model to load
 - <b>`output_path`</b> (str):  ouput to store the transpiled model. Defaults to "cairo_model".
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION(False).



**Raises:**

 - <b>`BadZipFile`</b>:  if the recieved file is not a zip, could be due to a transpilation error at the API.
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX
