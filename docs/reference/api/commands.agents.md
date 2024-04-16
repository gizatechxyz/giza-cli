<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/agents.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `commands.agents`




**Global Variables**
---------------
- **API_HOST**

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/agents.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create`

```python
create(
    model_id: int = typer.Option(
        None,
        "--model-id",
        "-m",
        help="The ID of the model used to create the agent",
    ),
    version_id: int = typer.Option(
        None,
        "--version-id",
        "-v",
        help="The ID of the version used to create the agent",
    ),
    endpoint_id: int = typer.Option(
        None,
        "--endpoint-id",
        "-e",
        help="The ID of the endpoint used to create the agent",
    ),
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="The name of the agent"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="The description of the agent"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/agents.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `list`

```python
list(
    parameters: Optional[List[str]] = typer.Option(
        None, "--parameters", "-p", help="The parameters of the agent"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/agents.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get`

```python
get(
    agent_id: int = typer.Option(
        None,
        "--agent-id",
        "-a",
        help="The ID of the agent",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/agents.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `delete_agent`

```python
delete_agent(
    agent_id: int = typer.Option(
        None,
        "--agent-id",
        "-a",
        help="The ID of the agent",
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/commands/agents.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update`

```python
update(
    agent_id: int = typer.Option(
        None,
        "--agent-id",
        "-a",
        help="The ID of the agent",
    ),
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="The name of the agent"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="The description of the agent"
    ),
    parameters: Optional[List[str]] = typer.Option(
        None, "--parameters", "-p", help="The parameters of the agent"
    ),
    debug: Optional[bool] = DEBUG_OPTION,
) → None
```






