# API Overview

## Modules

* [`callbacks`](callbacks.md#module-callbacks)
* [`cli`](cli.md#module-cli)
* [`client`](client.md#module-client)
* [`commands`](commands.md#module-commands)
* [`commands.actions`](../../docs/reference/api/commands.actions.md#module-commandsactions)
* [`commands.deployments`](../../docs/reference/api/commands.deployments.md#module-commandsdeployments)
* [`commands.models`](commands.models.md#module-commandsmodels)
* [`commands.prove`](commands.prove.md#module-commandsprove)
* [`commands.reset_password`](commands.reset\_password.md#module-commandsreset\_password)
* [`commands.users`](commands.users.md#module-commandsusers)
* [`commands.verify`](../../docs/reference/api/commands.verify.md#module-commandsverify)
* [`commands.version`](commands.version.md#module-commandsversion)
* [`commands.versions`](commands.versions.md#module-commandsversions)
* [`commands.workspaces`](commands.workspaces.md#module-commandsworkspaces)
* [`exceptions`](exceptions.md#module-exceptions)
* [`frameworks`](../../docs/reference/api/frameworks.md#module-frameworks)
* [`frameworks.cairo`](../../docs/reference/api/frameworks.cairo.md#module-frameworkscairo)
* [`frameworks.ezkl`](../../docs/reference/api/frameworks.ezkl.md#module-frameworksezkl)
* [`options`](options.md#module-options)
* [`utils`](utils.md#module-utils)
* [`utils.decorators`](utils.decorators.md#module-utilsdecorators)
* [`utils.echo`](utils.echo.md#module-utilsecho)
* [`utils.enums`](../../docs/reference/api/utils.enums.md#module-utilsenums)
* [`utils.misc`](../../docs/reference/api/utils.misc.md#module-utilsmisc)

## Classes

* [`client.ApiClient`](client.md#class-apiclient): Implementation of the API client to interact with core-services
* [`client.DeploymentsClient`](client.md#class-deploymentsclient): Client to interact with `deployments` endpoint.
* [`client.JobsClient`](client.md#class-jobsclient): Client to interact with `jobs` endpoint.
* [`client.ModelsClient`](client.md#class-modelsclient): Client to interact with `models` endpoint.
* [`client.ProofsClient`](client.md#class-proofsclient): Client to interact with `proofs` endpoint.
* [`client.TranspileClient`](client.md#class-transpileclient): Client to interact with `users` endpoint.
* [`client.UsersClient`](client.md#class-usersclient): Client to interact with `users` endpoint.
* [`client.VersionJobsClient`](client.md#class-versionjobsclient): Client to interact with `jobs` endpoint.
* [`client.VersionsClient`](client.md#class-versionsclient): Client to interact with `versions` endpoint.
* [`client.WorkspaceClient`](client.md#class-workspaceclient): Client to interact with `workspaces` endpoint.
* [`exceptions.PasswordError`](exceptions.md#class-passworderror)
* [`echo.Echo`](utils.echo.md#class-echo): Helper class to use when printing output of the CLI.
* [`enums.Framework`](../../docs/reference/api/utils.enums.md#class-framework)
* [`enums.JobKind`](../../docs/reference/api/utils.enums.md#class-jobkind)
* [`enums.JobSize`](../../docs/reference/api/utils.enums.md#class-jobsize)
* [`enums.JobStatus`](../../docs/reference/api/utils.enums.md#class-jobstatus)
* [`enums.ServiceSize`](../../docs/reference/api/utils.enums.md#class-servicesize)
* [`enums.VersionStatus`](../../docs/reference/api/utils.enums.md#class-versionstatus)

## Functions

* [`callbacks.debug_callback`](callbacks.md#function-debug\_callback): If a call adds the `--debug` flag debugging mode is activated for external requests and API Clients.
* [`callbacks.version_callback`](callbacks.md#function-version\_callback): Prints the current version when `--version` flag is added to a call.
* [`cli.entrypoint`](cli.md#function-entrypoint)
* [`actions.new`](../../docs/reference/api/commands.actions.md#function-new): This command will create a new action by generating a Python project.
* [`deployments.deploy`](../../docs/reference/api/commands.deployments.md#function-deploy)
* [`deployments.get`](../../docs/reference/api/commands.deployments.md#function-get)
* [`deployments.list`](../../docs/reference/api/commands.deployments.md#function-list)
* [`models.create`](commands.models.md#function-create): Command to create a model. Asks for the new model's information and validates the input,
* [`models.get`](commands.models.md#function-get): Command to create a user. Asks for the new users information and validates the input,
* [`models.list`](commands.models.md#function-list): Command to list all models.
* [`prove.prove`](commands.prove.md#function-prove)
* [`reset_password.handle_http_error`](commands.reset\_password.md#function-handle\_http\_error): Handle an HTTP error.
* [`reset_password.prompt_for_input`](commands.reset\_password.md#function-prompt\_for\_input): Prompt the user for input.
* [`reset_password.request_reset_password_token`](commands.reset\_password.md#function-request\_reset\_password\_token): Request a password reset token for a given email.
* [`reset_password.reset_password`](commands.reset\_password.md#function-reset\_password): Reset the password for a user using a reset token.
* [`users.create`](commands.users.md#function-create): Command to create a user. Asks for the new users information and validates the input,
* [`users.create_api_key`](commands.users.md#function-create\_api\_key): Create an API key for your user. You need to be logged in to create an API key.
* [`users.login`](commands.users.md#function-login): Logs the current user into Giza. Under the hood this will retrieve the token for the next requests.
* [`users.me`](commands.users.md#function-me): Retrieve information about the current user and print it as json to stdout.
* [`users.resend_email`](commands.users.md#function-resend\_email): Command to resend verification email. Asks for the user's email and sends the request to the API
* [`verify.verify`](../../docs/reference/api/commands.verify.md#function-verify)
* [`version.check_version`](commands.version.md#function-check\_version): Check if there is a new version available of the cli in pypi to suggest upgrade
* [`versions.download`](commands.versions.md#function-download): Retrieve information about the current user and print it as json to stdout.
* [`versions.download_original`](commands.versions.md#function-download\_original): Retrieve information about the current user and print it as json to stdout.
* [`versions.get`](commands.versions.md#function-get)
* [`versions.list`](commands.versions.md#function-list)
* [`versions.transpile`](commands.versions.md#function-transpile)
* [`versions.update`](commands.versions.md#function-update)
* [`workspaces.create`](commands.workspaces.md#function-create): Command to create a Giza Workspace.
* [`workspaces.delete`](commands.workspaces.md#function-delete)
* [`workspaces.get`](commands.workspaces.md#function-get)
* [`cairo.deploy`](../../docs/reference/api/frameworks.cairo.md#function-deploy): Command to deploy a specific version of a model. This will create a deployment for the specified version and check the status, once it finishes if COMPLETED the deployment is ready to be used.
* [`cairo.prove`](../../docs/reference/api/frameworks.cairo.md#function-prove): Command to prove as spceific cairo program, previously converted to CASM.
* [`cairo.transpile`](../../docs/reference/api/frameworks.cairo.md#function-transpile): This function is responsible for transpiling a model. The overall objective is to prepare a model for use by converting it into a different format (transpiling).
* [`ezkl.prove`](../../docs/reference/api/frameworks.ezkl.md#function-prove)
* [`ezkl.setup`](../../docs/reference/api/frameworks.ezkl.md#function-setup): This function executes the setup of the model and creates the outputs, handled by Giza.
* [`ezkl.verify`](../../docs/reference/api/frameworks.ezkl.md#function-verify): Create a verification job.
* [`utils.get_response_info`](utils.md#function-get\_response\_info): Utility to retrieve information of the client response.
* [`decorators.auth`](utils.decorators.md#function-auth): Check that we have the token and it is not expired before executing
