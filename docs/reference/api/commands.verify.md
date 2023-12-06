<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/verify.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.verify`





---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/verify.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `verify`

```python
verify(
    model_id: Optional[int] = typer.Option(None, "--model-id", "-m"),
    version_id: Optional[int] = typer.Option(None, "--version-id", "-v"),
    proof_id: Optional[int] = typer.Option(None, "--proof-id", "-p"),
    proof: Optional[str] = typer.Option(None, "--proof", "-P"),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    framework: Framework = typer.Option(Framework.CAIRO, "--framework", "-f"),
    debug: Optional[bool] = DEBUG_OPTION
) → None
```






