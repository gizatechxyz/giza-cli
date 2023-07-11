<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.decorators`




**Global Variables**
---------------
- **TYPE_CHECKING**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `auth`

```python
auth(func: Callable)
```

Check that we have the token and it is not expired before executing

Expects to be called from an instance of ApiClient to and endpoint that needs authorization



**Args:**

 - <b>`func`</b> (Callable):  function to decorate



**Returns:**

 - <b>`Callable`</b>:  decorated function
