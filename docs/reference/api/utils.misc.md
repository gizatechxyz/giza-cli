<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.misc`





---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_model_or_sierra`

```python
download_model_or_sierra(
    content: bytes,
    output_path: str,
    name: Optional[str] = None
)
```

Download the model or sierra file. 



**Args:**
 
 - <b>`content`</b> (bytes):  file content 
 - <b>`output_path`</b> (str):  path to save the file 
 - <b>`name`</b> (str):  file name. Defaults to None. 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `zip_folder`

```python
zip_folder(source_folder: str, dst_folder: str) → str
```

Zip the folder to a specific location. 



**Args:**
 
 - <b>`source_folder`</b> (str):  path to the folder 
 - <b>`dst_folder`</b> (str):  destination folder 



**Returns:**
 
 - <b>`str`</b>:  path to the zip file 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `scarb_build`

```python
scarb_build(folder) → None
```

Build the scarb model. 



**Args:**
 
 - <b>`folder`</b> (str):  path to the folder 


