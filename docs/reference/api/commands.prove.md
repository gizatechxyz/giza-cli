<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/prove.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.prove`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/prove.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prove`

```python
prove(
    program: str = typer.Argument(None),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    output_path: str = typer.Option("zk.proof", "--output-path", "-o"),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```

Command to prove as spceific cairo program, previously converted to CASM. This will create a proving job and check the status, once it finishes if COMPLETED the proof is downloaded at the output path The daily jobs allowed are rate limited by the backend. 



**Args:**
 
 - <b>`program`</b>:  main CASM file 
 - <b>`size`</b>:  Size of the job, allowed values are S, M, L and XL. Defaults to S. 
 - <b>`output_path`</b>:  output path of the zk proof generated in the job 
 - <b>`debug`</b> (Optional[bool], optional):  Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False). 



**Raises:**
 
 - <b>`ValidationError`</b>:  input fields are validated, if these are not suitable the exception is raised 
 - <b>`HTTPError`</b>:  request error to the API, 4XX or 5XX 


