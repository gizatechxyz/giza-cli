<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/frameworks/cairo.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `frameworks.cairo`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/frameworks/cairo.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prove`

```python
prove(
    data: str,
    debug: Optional[bool],
    size: JobSize = <JobSize.S: 'S'>,
    framework: Framework = <Framework.CAIRO: 'CAIRO'>,
    output_path: str = 'zk.proof'
) → None
```

Command to prove as spceific cairo program, previously converted to CASM. This will create a proving job and check the status, once it finishes if COMPLETED the proof is downloaded at the output path The daily jobs allowed are rate limited by the backend. 



**Args:**
 
 - <b>`data`</b>:  main CASM file 
 - <b>`size`</b>:  Size of the job, allowed values are S, M, L and XL. Defaults to S. 
 - <b>`output_path`</b>:  output path of the zk proof generated in the job 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False). 



**Raises:**
 
 - <b>`ValidationError`</b>:  input fields are validated, if these are not suitable the exception is raised 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/frameworks/cairo.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `transpile`

```python
transpile(
    model_path: str,
    model_id: int,
    desc: str,
    model_desc: str,
    output_path: str,
    debug: Optional[bool]
) → None
```

This function is responsible for transpiling a model. The overall objective is to prepare a model for use by converting it into a different format (transpiling). The function performs the following steps: 

1. Checks if a model_id is provided. If not, it extracts the model_name from the model_path. 2. If a model description is provided and a model_id is also provided, it ignores the provided description. 3. It then attempts to retrieve the model. If the model does not exist, it creates a new one. 4. The function then creates a new version for the model, uploads the model file, and updates the status to UPLOADED. 5. It then continuously checks the status of the version until it is either COMPLETED or FAILED. 6. If the status is COMPLETED, it downloads the model to the specified path. 7. If any errors occur during this process, they are handled and appropriate error messages are displayed. 



**Args:**
 
 - <b>`model_path`</b> (str):  Path of the model to transpile. 
 - <b>`model_id`</b> (int, optional):  The ID of the model where a new version will be created. Defaults to None. 
 - <b>`desc`</b> (int, optional):  Description of the version. Defaults to None. 
 - <b>`model_desc`</b> (int, optional):  Description of the Model to create if model_id is not provided. Defaults to None. 
 - <b>`output_path`</b> (str, optional):  The path where the cairo model will be saved. Defaults to "cairo_model". 
 - <b>`debug`</b> (bool, optional):  A flag used to determine whether to raise exceptions or not. Defaults to DEBUG_OPTION. 



**Raises:**
 
 - <b>`ValidationError`</b>:  If there is a validation error with the model or version. 
 - <b>`HTTPError`</b>:  If there is an HTTP error while communicating with the server. 


