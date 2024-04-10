<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.misc`





---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `scarb_build`

```python
scarb_build(folder) → None
```

Build the scarb model. 



**Args:**
 
 - <b>`folder`</b> (str):  path to the folder 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_ape_accounts`

```python
get_ape_accounts() → Dict[str, Path]
```

Get the available APE accounts. 



**Returns:**
 
 - <b>`list`</b>:  list of available APE accounts 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_parameters_from_str`

```python
get_parameters_from_str(parameters: List[str]) → Dict[str, str]
```

Get the parameters from a string. 



**Args:**
 
 - <b>`parameters`</b> (List[str]):  parameters 



**Returns:**
 
 - <b>`Dict[str, str]`</b>:  parameters 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/misc.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_json_file`

```python
load_json_file(file_path: str) → Dict
```

Load a json file. 



**Args:**
 
 - <b>`file_path`</b> (str):  path to the file 



**Returns:**
 
 - <b>`Dict`</b>:  json content 


