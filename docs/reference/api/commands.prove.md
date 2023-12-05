<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/prove.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.prove`





---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/prove.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prove`

```python
prove(
    data: str = typer.Argument(None),
    model_id: Optional[str] = typer.Option(None, "--model-id", "-m"),
    version_id: Optional[str] = typer.Option(None, "--version-id", "-v"),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    framework: Framework = typer.Option(Framework.CAIRO, "--framework", "-f"),
    output_path: str = typer.Option("zk.proof", "--output-path", "-o"),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






