<!-- markdownlint-disable -->

# API Overview

## Modules

- [`callbacks`](./callbacks.md#module-callbacks)
- [`cli`](./cli.md#module-cli)
- [`client`](./client.md#module-client)
- [`commands`](./commands.md#module-commands)
- [`commands.models`](./commands.models.md#module-commandsmodels)
- [`commands.prove`](./commands.prove.md#module-commandsprove)
- [`commands.reset_password`](./commands.reset_password.md#module-commandsreset_password)
- [`commands.transpile`](./commands.transpile.md#module-commandstranspile)
- [`commands.users`](./commands.users.md#module-commandsusers)
- [`commands.version`](./commands.version.md#module-commandsversion)
- [`exceptions`](./exceptions.md#module-exceptions)
- [`options`](./options.md#module-options)
- [`utils`](./utils.md#module-utils)
- [`utils.decorators`](./utils.decorators.md#module-utilsdecorators)
- [`utils.echo`](./utils.echo.md#module-utilsecho)
- [`utils.enums`](./utils.enums.md#module-utilsenums)
- [`utils.misc`](./utils.misc.md#module-utilsmisc)

## Classes

- [`client.ApiClient`](./client.md#class-apiclient): Implementation of the API client to interact with core-services
- [`client.JobsClient`](./client.md#class-jobsclient): Client to interact with `jobs` endpoint.
- [`client.ModelsClient`](./client.md#class-modelsclient): Client to interact with `models` endpoint.
- [`client.ProofsClient`](./client.md#class-proofsclient): Client to interact with `proofs` endpoint.
- [`client.TranspileClient`](./client.md#class-transpileclient): Client to interact with `users` endpoint.
- [`client.UsersClient`](./client.md#class-usersclient): Client to interact with `users` endpoint.
- [`exceptions.PasswordError`](./exceptions.md#class-passworderror)
- [`echo.Echo`](./utils.echo.md#class-echo): Helper class to use when printin output of the CLI.
- [`enums.JobSize`](./utils.enums.md#class-jobsize)
- [`enums.JobStatus`](./utils.enums.md#class-jobstatus)
- [`enums.ModelStatus`](./utils.enums.md#class-modelstatus)

## Functions

- [`callbacks.debug_callback`](./callbacks.md#function-debug_callback): If a call adds the `--debug` flag debugging mode is activated for external requests and API Clients.
- [`callbacks.version_callback`](./callbacks.md#function-version_callback): Prints the current version when `--version` flag is added to a call.
- [`cli.entrypoint`](./cli.md#function-entrypoint)
- [`models.download`](./commands.models.md#function-download): Retrieve information about the current user and print it as json to stdout.
- [`models.get`](./commands.models.md#function-get): Command to create a user. Asks for the new users information and validates the input,
- [`prove.prove`](./commands.prove.md#function-prove): Command to prove as spceific cairo program, previously converted to CASM.
- [`reset_password.handle_http_error`](./commands.reset_password.md#function-handle_http_error): Handle an HTTP error.
- [`reset_password.prompt_for_input`](./commands.reset_password.md#function-prompt_for_input): Prompt the user for input.
- [`reset_password.request_reset_password_token`](./commands.reset_password.md#function-request_reset_password_token): Request a password reset token for a given email.
- [`reset_password.reset_password`](./commands.reset_password.md#function-reset_password): Reset the password for a user using a reset token.
- [`transpile.transpile`](./commands.transpile.md#function-transpile): Command to transpile the model using the client. Sends the model and then unzips it to the desired location.
- [`users.create`](./commands.users.md#function-create): Command to create a user. Asks for the new users information and validates the input,
- [`users.login`](./commands.users.md#function-login): Logs the current user into Giza. Under the hood this will retrieve the token for the next requests.
- [`users.me`](./commands.users.md#function-me): Retrieve information about the current user and print it as json to stdout.
- [`version.version_entrypoint`](./commands.version.md#function-version_entrypoint): Prints the current CLI version.
- [`utils.get_response_info`](./utils.md#function-get_response_info): Utility to retrieve information of the client response.
- [`decorators.auth`](./utils.decorators.md#function-auth): Check that we have the token and it is not expired before executing
