# Workspaces

Workspaces in our platform are a crucial component designed to enhance user interaction with Giza Actions. These workspaces provide a user-friendly interface (UI) for managing and tracking runs, tasks, and metadata associated with action executions. Leveraging a command-line interface (CLI), users can seamlessly interact with workspaces, ensuring a smooth and efficient experience.

The incorporation of Workspaces stems from our commitment to optimizing user interaction with Giza Actions. These dedicated workspaces serve as a strategic enhancement, providing a cohesive environment for users to oversee, manage, and delve into the intricate details of action runs, tasks, and associated metadata. The introduction of Workspaces aims to elevate user efficiency, offering a centralized hub that streamlines navigation and organization.

## Create a Workspace

To create a new workspace, users can utilize the giza workspace create command. This command initiates the creation process, setting up a new workspace. If a workspace with the specified name already exists, the command will gracefully handle this scenario by throwing an error, ensuring that each workspace has a unique identifier.

The workspace creation process can take up to 10 minutes as we are creating isolated resources for each respective workspace.

```console
> giza workspaces create
[giza][2024-01-17 14:40:02.046] Creating Workspace ✅ 
[WARNING][2024-01-17 14:40:02.047] This process can take up to 10 minutes ⏳
[giza][2024-01-17 14:41:51.248] Waiting for workspace creation...
[giza][2024-01-17 14:43:12.291] Workspace status is 'PROCESSING'
[giza][2024-01-17 14:45:54.365] Worksace creation is successful ✅
[giza][2024-01-17 14:45:54.366] ✅ Workspace URL: https://actions-server-gizabrain-gageadsga-ew.a.run.app ✅
```

Once created, the workspace will be available for use. The workspace URL will be printed in the console, and it can be used to access the workspace.

![workspace](../.gitbook/assets/workspace.png)

Now you can start using the workspace to run actions!

## Retrieve a Workspace

For retrieving information about an existing workspace, the giza workspace get command comes into play. This command provides users with a comprehensive overview of the specified workspace, including details about the url. It serves as a quick reference point to get the workspace URL for the user.

```console
> giza workspaces get
[giza][2024-01-17 14:46:35.654] Retrieving workspace information ✅ 
[giza][2024-01-17 14:46:35.805] ✅ Workspace URL: https://actions-server-gizabrain-gageadsga-ew.a.run.app ✅
{
  "url": "https://actions-server-gizabrain-gageadsga-ew.a.run.app",
  "status": "COMPLETED"
}
```

## Delete a Workspace

In situations where a workspace is no longer needed, users can use the giza workspace delete command to remove it. This command ensures a clean and straightforward deletion process for an existing workspace, allowing users to manage their resources efficiently.

It will prompt a confirmation message before deleting the workspace as **USER DATA WILL BE ERASED**.

```console
> giza workspaces delete
[WARNING][2024-01-17 14:48:29.103] THIS WILL ERASE ALL YOUR WORKSPACE DATA ❌
Are you sure you want to delete the workspace? [y/N]: y
[giza][2024-01-17 14:49:05.777] Deleting Workspace ✅ 
[giza][2024-01-17 14:49:08.507] Workspace Deleted ✅
```

## About Giza Actions

Giza Actions is the core component within the platform, Workspaces act as an interface to connect with these actions, providing users with a centralized hub to monitor and manage their executions. This integration enhances the overall usability and accessibility of Giza Actions, making it easier for users to interact with and control their workflows.

By integrating workspaces into our platform, we aim to simplify the user experience, offering a powerful yet intuitive solution for managing Giza Actions effectively.

The Actions-SDK can be found at: [https://actions.gizatech.xyz/welcome/giza-actions-sdk](https://actions.gizatech.xyz/welcome/giza-actions-sdk)
