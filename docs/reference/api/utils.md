<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/__init__.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils`





---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/__init__.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_response_info`

```python
get_response_info(response: Response) → Dict[str, Any]
```

Utility to retrieve information of the client response.

Try to get the body, if not just get the text.



**Args:**

 - <b>`response`</b> (Response):  a response from the API



**Returns:**

 - <b>`dict`</b>:  information about the returned response
