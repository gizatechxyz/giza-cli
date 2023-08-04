<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/transpile.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.transpile`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/transpile.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `transpile`

```python
transpile(
    model_path: str = typer.Argument(None, help="Path of the model to transpile"),
    output_path: str = typer.Option(
        "cairo_model", "--output-path", "-o", help="Path to output the cairo model"
    )
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```

Command to transpile the model using the client. Sends the model and then unzips it to the desired location. 

This command will do a couple of things behind the scenes:  * Create a Model entity  * Upload the model  * Update the status of the model  * Poll the model until the status is either FAILED or COMPLETED  * If COMPLETED the model is downloaded 



**Args:**
 
 - <b>`model_path`</b> (str):  path for the model to load 
 - <b>`output_path`</b> (str):  ouput to store the transpiled model. Defaults to "cairo_model". 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests,  extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION(False). 



**Raises:**
 
 - <b>`BadZipFile`</b>:  if the recieved file is not a zip, could be due to a transpilation error at the API. 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


