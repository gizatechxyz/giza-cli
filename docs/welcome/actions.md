# Actions

Build Verifiable ML products with ease.

Giza Actions empowers developers to build and scale Verifiable ML solutions quickly, turning their python scripts and ML models into resilient, recurrent workflows. Every model contained in an Action has verifiability properties without any code change using ZKML with  and Giza Platform.

At the core of Giza Actions are Actions themselves. An action serves as a framework for coding ML inferencing workflow logic, enabling users to tailor the behaviour of their workflows. Defined as Python functions, any Python function has the potential to be transformed into an action.

More information about Giza Actions can be found in the [Actions Documentation](https://actions.gizatech.xyz/concepts/actions).

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

## Related Topics

- [Actions SDK](https://actions.gizatech.xyz/welcome/giza-actions-sdk)
- [Workspace](../resources/workspaces.md)
- [Models](../resources/models.md)
- [Versions](../resources/versions.md)
