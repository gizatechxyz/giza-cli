<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/endpoints.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.endpoints`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/endpoints.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `deploy`

```python
deploy(
    data: str = typer.Argument(None),
    model_id: int = typer.Option(
        None,
        "--model-id",
        "-m",
        help="The ID of the model where an endpoint will be created",
    ),
    version_id: int = typer.Option(
        None,
        "--version-id",
        "-v",
        help="The ID of the version that will used in the endpoint",
    ),
    size: ServiceSize = typer.Option(ServiceSize.S, "--size", "-s"),
    framework: Framework = typer.Option(Framework.CAIRO, "--framework", "-f"),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/endpoints.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `list`

```python
list(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/endpoints.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get`

```python
get(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/endpoints.py#L160"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `list_proofs`

```python
list_proofs(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/endpoints.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_proof`

```python
get_proof(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    proof_id: str = typer.Option(
        None, "--proof-id", "-p", help="The ID or request id of the proof"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/endpoints.py#L263"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_proof`

```python
download_proof(
    model_id: int = typer.Option(None, "--model-id", "-m", help="The ID of the model"),
    version_id: int = typer.Option(
        None, "--version-id", "-v", help="The ID of the version"
    ),
    endpoint_id: int = typer.Option(
        None,
        "--deployment-id",
        "-d",
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint",
    ),
    proof_id: str = typer.Option(
        None, "--proof-id", "-p", help="The ID or request id of the proof"
    ),
    output_path: str = typer.Option(
        "zk.proof",
        "--output-path",
        "-o",
        help="The path where the proof will be stored",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






