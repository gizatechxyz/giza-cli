<!-- markdownlint-disable -->

# API Overview

## Modules

- [`callbacks`](./callbacks.md#module-callbacks)
- [`cli`](./cli.md#module-cli)
- [`client`](./client.md#module-client)
- [`commands`](./commands.md#module-commands)
- [`commands.transpile`](./commands.transpile.md#module-commandstranspile)
- [`commands.users`](./commands.users.md#module-commandsusers)
- [`commands.version`](./commands.version.md#module-commandsversion)
- [`options`](./options.md#module-options)
- [`utils`](./utils.md#module-utils)
- [`utils.decorators`](./utils.decorators.md#module-utilsdecorators)
- [`utils.echo`](./utils.echo.md#module-utilsecho)

## Classes

- [`client.ApiClient`](./client.md#class-apiclient): Implementation of the API client to interact with core-services
- [`client.TranspileClient`](./client.md#class-transpileclient): Client to interact with `users` endpoint.
- [`client.UsersClient`](./client.md#class-usersclient): Client to interact with `users` endpoint.
- [`echo.Echo`](./utils.echo.md#class-echo): Helper class to use when printin output of the CLI.

## Functions

- [`callbacks.debug_callback`](./callbacks.md#function-debug_callback): If a call adds the `--debug` flag debugging mode is activated for external requests and API Clients.
- [`callbacks.version_callback`](./callbacks.md#function-version_callback): Prints the current version when `--version` flag is added to a call.
- [`cli.entrypoint`](./cli.md#function-entrypoint)
- [`transpile.transpile`](./commands.transpile.md#function-transpile): Command to transpile the model using the client. Sends the model and then unzips it to the desired location.
- [`users.create`](./commands.users.md#function-create): Command to create a user. Asks for the new users information and validates the input,
- [`users.login`](./commands.users.md#function-login): Logs the current user to Giza Platform. Under the hood this will retrieve the token for the next requests.
- [`users.me`](./commands.users.md#function-me): Retrieve information about the current user and print it as json to stdout.
- [`version.version_entrypoint`](./commands.version.md#function-version_entrypoint): Prints the current CLI version.
- [`utils.get_response_info`](./utils.md#function-get_response_info): Utility to retrieve information of the client response.
- [`decorators.auth`](./utils.decorators.md#function-auth): Check that we have the token and it is not expired before executing
