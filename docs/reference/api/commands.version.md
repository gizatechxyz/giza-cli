<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/version.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.version`





---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/version.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `version_entrypoint`

```python
version_entrypoint(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    )
) → None
```

Prints the current CLI version. 



**Args:**
 
 - <b>`version`</b> (bool):  Tper callback to retrieve the version. 


