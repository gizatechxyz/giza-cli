<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/exception_handling.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.exception_handling`






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/exception_handling.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ExceptionHandler`
Context manager to handle exceptions in the CLI. 

The main purpose of this class is to handle common exceptions in the CLI and provide a consistent way to handle them. 

The CLI commands should be wrapped with this context manager to handle exceptions and provide a consistent way to handle them. 



**Example:**
 ```python
with ExceptionHandler():
     # Your command code here
     client = Client()
     client.get() # This will raise an exception if something goes wrong but will be handled in __exit__
``` 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/exception_handling.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(debug: Optional[bool] = False) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/exception_handling.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle_exit`

```python
handle_exit()
```






