<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/frameworks/ezkl.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `frameworks.ezkl`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/frameworks/ezkl.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `setup`

```python
setup(
    model_path: str,
    model_id: int,
    desc: str,
    model_desc: str,
    input_data: str,
    debug: Optional[bool],
    size: JobSize = <JobSize.S: 'S'>
) → None
```

This function executes the setup of the model and creates the outputs, handled by Giza. It first checks if the input data is provided. If not, it prints an error message and exits the program. If the model ID is not provided, it checks if the model exists and uses it if it does, or creates a new one if it doesn't. It then retrieves the model, creates a version, sends the model for setup, and creates a setup job. It keeps checking the status of the job until it is completed or fails. If the job validation fails or there is an HTTP error, it prints an error message and exits the program. 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/frameworks/ezkl.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prove`

```python
prove(
    model_id: Optional[int],
    version_id: Optional[int],
    input_data: str,
    output_path: str,
    debug: Optional[bool],
    size: JobSize = <JobSize.S: 'S'>
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/frameworks/ezkl.py#L228"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `verify`

```python
verify(
    proof_id: Optional[int],
    model_id: Optional[int],
    version_id: Optional[int],
    proof: Optional[str] = None,
    debug: Optional[bool] = False,
    size: JobSize = <JobSize.S: 'S'>
)
```

Create a verification job. This command will create a verification job with the provided proof id. The job size, model id, and version id can be optionally specified. 


