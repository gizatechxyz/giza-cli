# Actions

Actions within the Giza Platform are a powerful suite of services designed to maximize the potential of the platform by integrating Verifiable Machine Learning (ML). These services operate in conjunction with platform versions and are orchestrated using the `actions-sdk`. With the ability to create, deploy, and monitor actions, users can harness the full capabilities of the Giza Platform while ensuring verifiable and secure ML processes.

Actions play a pivotal role in the Giza Platform by extending its functionality beyond basic version creation. By leveraging Verifiable ML, actions empower users to perform intricate tasks and analyses on the platform, ensuring that machine learning processes are not only accurate but also verifiable. This capability is essential for maintaining transparency, security, and accountability in machine learning workflows, especially in applications where trust and verifiability are critical.

## Starting with Actions

Jumpstarting the creation of actions is made efficient through the use of a template powered by Cookiecutter. This template serves as a foundation for creating actions and pipelines, streamlining the development process. The `actions-sdk` provides the necessary tools to create, visualize, and monitor these pipelines, enabling users to deploy and manage their actions seamlessly.

```console
> giza actions new actions_project
[giza][2024-01-18 11:38:43.180] Creating a new Action project with name: actions_project ✅ 
[giza][2024-01-18 11:38:44.173] Action project created successfully at ./actions_project ✅
```

This will create a new directory with the following structure:

```console
> tree actions_project
actions_project
├── README.md
├── actions_project
│   ├── __init__.py
│   └── action.py
├── pyproject.toml
└── tests
    └── __init__.py

3 directories, 5 files
```

This will contain a minimul setup to help you get started with your action. For example, the `action.py` file will contain the following:

```python
from giza_actions.action import Action, action
from giza_actions.model import GizaModel
from giza_actions.task import task

@task
def preprocess():
    print(f"Preprocessing...")


@task
def transform():
    print(f"Transforming...")


@action(log_prints=True, verifiable=True)
def inference():
    preprocess()
    transform()

if __name__ == '__main__':
    action_deploy = Action(entrypoint=inference, name="inference-local-action")
    action_deploy.serve(name="inference-local-action")
```

## Related Topics

- [Actions SDK](https://github.com/gizatechxyz/actions-sdk)
- [Workspace](../resources/workspaces.md)
- [Models](../resources/models.md)
- [Versions](../resources/versions.md)
