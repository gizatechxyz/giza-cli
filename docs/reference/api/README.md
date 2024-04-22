<!-- markdownlint-disable -->

# API Overview

## Modules

- [`callbacks`](./callbacks.md#module-callbacks)
- [`cli`](./cli.md#module-cli)
- [`client`](./client.md#module-client)
- [`commands`](./commands.md#module-commands)
- [`commands.actions`](./commands.actions.md#module-commandsactions)
- [`commands.agents`](./commands.agents.md#module-commandsagents)
- [`commands.endpoints`](./commands.endpoints.md#module-commandsendpoints)
- [`commands.models`](./commands.models.md#module-commandsmodels)
- [`commands.prove`](./commands.prove.md#module-commandsprove)
- [`commands.reset_password`](./commands.reset_password.md#module-commandsreset_password)
- [`commands.users`](./commands.users.md#module-commandsusers)
- [`commands.verify`](./commands.verify.md#module-commandsverify)
- [`commands.version`](./commands.version.md#module-commandsversion)
- [`commands.versions`](./commands.versions.md#module-commandsversions)
- [`commands.workspaces`](./commands.workspaces.md#module-commandsworkspaces)
- [`exceptions`](./exceptions.md#module-exceptions)
- [`frameworks`](./frameworks.md#module-frameworks)
- [`frameworks.cairo`](./frameworks.cairo.md#module-frameworkscairo)
- [`frameworks.ezkl`](./frameworks.ezkl.md#module-frameworksezkl)
- [`options`](./options.md#module-options)
- [`utils`](./utils.md#module-utils)
- [`utils.decorators`](./utils.decorators.md#module-utilsdecorators)
- [`utils.echo`](./utils.echo.md#module-utilsecho)
- [`utils.enums`](./utils.enums.md#module-utilsenums)
- [`utils.exception_handling`](./utils.exception_handling.md#module-utilsexception_handling)
- [`utils.misc`](./utils.misc.md#module-utilsmisc)

## Classes

- [`client.AgentsClient`](./client.md#class-agentsclient): Client to interact with `agents` endpoint.
- [`client.ApiClient`](./client.md#class-apiclient): Implementation of the API client to interact with core-services
- [`client.EndpointsClient`](./client.md#class-endpointsclient): Client to interact with `endpoints` endpoint.
- [`client.EndpointsClient`](./client.md#class-endpointsclient): Client to interact with `endpoints` endpoint.
- [`client.JobsClient`](./client.md#class-jobsclient): Client to interact with `jobs` endpoint.
- [`client.ModelsClient`](./client.md#class-modelsclient): Client to interact with `models` endpoint.
- [`client.ProofsClient`](./client.md#class-proofsclient): Client to interact with `proofs` endpoint.
- [`client.TranspileClient`](./client.md#class-transpileclient): Client to interact with `users` endpoint.
- [`client.UsersClient`](./client.md#class-usersclient): Client to interact with `users` endpoint.
- [`client.VersionJobsClient`](./client.md#class-versionjobsclient): Client to interact with `jobs` endpoint.
- [`client.VersionsClient`](./client.md#class-versionsclient): Client to interact with `versions` endpoint.
- [`client.WorkspaceClient`](./client.md#class-workspaceclient): Client to interact with `workspaces` endpoint.
- [`exceptions.PasswordError`](./exceptions.md#class-passworderror)
- [`exceptions.ScarbBuildError`](./exceptions.md#class-scarbbuilderror)
- [`exceptions.ScarbNotFound`](./exceptions.md#class-scarbnotfound)
- [`echo.Echo`](./utils.echo.md#class-echo): Helper class to use when printin output of the CLI.
- [`enums.Framework`](./utils.enums.md#class-framework)
- [`enums.JobKind`](./utils.enums.md#class-jobkind)
- [`enums.JobSize`](./utils.enums.md#class-jobsize)
- [`enums.JobStatus`](./utils.enums.md#class-jobstatus)
- [`enums.ServiceSize`](./utils.enums.md#class-servicesize)
- [`enums.VersionStatus`](./utils.enums.md#class-versionstatus)
- [`exception_handling.ExceptionHandler`](./utils.exception_handling.md#class-exceptionhandler): Context manager to handle exceptions in the CLI.

## Functions

- [`callbacks.debug_callback`](./callbacks.md#function-debug_callback): If a call adds the `--debug` flag debugging mode is activated for external requests and API Clients.
- [`callbacks.version_callback`](./callbacks.md#function-version_callback): Prints the current version when `--version` flag is added to a call.
- [`cli.entrypoint`](./cli.md#function-entrypoint)
- [`actions.new`](./commands.actions.md#function-new): This command will create a new action by generating a Python project.
- [`agents.create`](./commands.agents.md#function-create)
- [`agents.delete_agent`](./commands.agents.md#function-delete_agent)
- [`agents.get`](./commands.agents.md#function-get)
- [`agents.list`](./commands.agents.md#function-list)
- [`agents.update`](./commands.agents.md#function-update)
- [`endpoints.delete_endpoint`](./commands.endpoints.md#function-delete_endpoint)
- [`endpoints.deploy`](./commands.endpoints.md#function-deploy)
- [`endpoints.download_proof`](./commands.endpoints.md#function-download_proof)
- [`endpoints.get`](./commands.endpoints.md#function-get)
- [`endpoints.get_proof`](./commands.endpoints.md#function-get_proof)
- [`endpoints.list`](./commands.endpoints.md#function-list)
- [`endpoints.list_jobs`](./commands.endpoints.md#function-list_jobs)
- [`endpoints.list_proofs`](./commands.endpoints.md#function-list_proofs)
- [`endpoints.verify`](./commands.endpoints.md#function-verify)
- [`models.create`](./commands.models.md#function-create): Command to create a model. Asks for the new model's information and validates the input,
- [`models.get`](./commands.models.md#function-get): Command to create a user. Asks for the new users information and validates the input,
- [`models.list`](./commands.models.md#function-list): Command to list all models.
- [`prove.prove`](./commands.prove.md#function-prove)
- [`reset_password.handle_http_error`](./commands.reset_password.md#function-handle_http_error): Handle an HTTP error.
- [`reset_password.prompt_for_input`](./commands.reset_password.md#function-prompt_for_input): Prompt the user for input.
- [`reset_password.request_reset_password_token`](./commands.reset_password.md#function-request_reset_password_token): Request a password reset token for a given email.
- [`reset_password.reset_password`](./commands.reset_password.md#function-reset_password): Reset the password for a user using a reset token.
- [`users.create`](./commands.users.md#function-create): Command to create a user. Asks for the new users information and validates the input,
- [`users.create_api_key`](./commands.users.md#function-create_api_key): Create an API key for your user. You need to be logged in to create an API key.
- [`users.login`](./commands.users.md#function-login): Logs the current user into Giza. Under the hood this will retrieve the token for the next requests.
- [`users.me`](./commands.users.md#function-me): Retrieve information about the current user and print it as json to stdout.
- [`users.resend_email`](./commands.users.md#function-resend_email): Command to resend verification email. Asks for the user's email and sends the request to the API
- [`verify.verify`](./commands.verify.md#function-verify)
- [`version.check_version`](./commands.version.md#function-check_version): Check if there is a new version available of the cli in pypi to suggest upgrade
- [`versions.download`](./commands.versions.md#function-download): Retrieve information about the current user and print it as json to stdout.
- [`versions.download_original`](./commands.versions.md#function-download_original): Retrieve information about the current user and print it as json to stdout.
- [`versions.get`](./commands.versions.md#function-get)
- [`versions.list`](./commands.versions.md#function-list)
- [`versions.transpile`](./commands.versions.md#function-transpile)
- [`versions.update`](./commands.versions.md#function-update)
- [`versions.update_sierra`](./commands.versions.md#function-update_sierra)
- [`workspaces.create`](./commands.workspaces.md#function-create): Command to create a Giza Workspace.
- [`workspaces.delete`](./commands.workspaces.md#function-delete)
- [`workspaces.get`](./commands.workspaces.md#function-get)
- [`cairo.deploy`](./frameworks.cairo.md#function-deploy): Command to deploy a specific version of a model. This will create an endpoint for the specified version and check the status, once it finishes if COMPLETED the endpoint is ready to be used.
- [`cairo.prove`](./frameworks.cairo.md#function-prove): Command to prove as spceific cairo program, previously converted to CASM.
- [`cairo.transpile`](./frameworks.cairo.md#function-transpile): This function is responsible for transpiling a model. The overall objective is to prepare a model for use by converting it into a different format (transpiling).
- [`cairo.verify`](./frameworks.cairo.md#function-verify): Create a verification job.
- [`ezkl.deploy`](./frameworks.ezkl.md#function-deploy): Command to deploy a specific version of a model. This will create a endpoint for the specified version and check the status, once it finishes if COMPLETED the endpoint is ready to be used.
- [`ezkl.prove`](./frameworks.ezkl.md#function-prove)
- [`ezkl.setup`](./frameworks.ezkl.md#function-setup): This function executes the setup of the model and creates the outputs, handled by Giza.
- [`ezkl.verify`](./frameworks.ezkl.md#function-verify): Create a verification job.
- [`utils.get_response_info`](./utils.md#function-get_response_info): Utility to retrieve information of the client response.
- [`decorators.auth`](./utils.decorators.md#function-auth): Check that we have the token and it is not expired before executing
- [`misc.download_model_or_sierra`](./utils.misc.md#function-download_model_or_sierra): Download the model or sierra file.
- [`misc.get_ape_accounts`](./utils.misc.md#function-get_ape_accounts): Get the available APE accounts.
- [`misc.get_parameters_from_str`](./utils.misc.md#function-get_parameters_from_str): Get the parameters from a string.
- [`misc.load_json_file`](./utils.misc.md#function-load_json_file): Load a json file.
- [`misc.scarb_build`](./utils.misc.md#function-scarb_build): Build the scarb model.
- [`misc.zip_folder`](./utils.misc.md#function-zip_folder): Zip the folder to a specific location.
