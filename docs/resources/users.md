# Users

Giza CLI provides the capabilities to manage users in Giza.

- [Users](#users)
  - [Available commands](#available-commands)
    - [Create](#create)
    - [Login](#login)
    - [Create API Key](#create-api-key)
    - [Me](#me)

## Available commands

### Create

Allows to create a user using the CLI. The username must be unique and the email account should not have been used previously for another user.

```console
> giza users create

Enter your username 😎: my-username
Enter your password 🥷 : (this is a secret)
Enter your email 📧: gonzalo@gizatech.xyz
[giza][2023-06-23 12:29:41.417] User created ✅. Check for a verification email 📧
```

This will create an *inactive* user in Giza, to activate it you need to verify your user through the verification email.

If there is an error or you want to have more information about what it's going on there is a `--debug` flag that will add more information about the error. This will print outgoing requests to the API, debug logs and python traceback about what happened.

⚠️**Note**: be aware that the debug option will print everything that its going to the API, in this case the password will be printed as plain text in the terminal, if you are using the debug option to fill a issue make sure to remove the credentials.

### Login

Log into Giza platfrom and retieve a JWT for authentication. This JWT will be stored to authenticate you later until the token expires.

**You need te have an active account to log in**

```console
> giza users login

Enter your username 😎: my-username
Enter your password 🥷 :
[giza][2023-06-23 12:32:17.917] Log into Giza
[giza][2023-06-23 12:32:18.716] ⛔️Could not authorize the user⛔️
[giza][2023-06-23 12:32:18.718] ⛔️Status code -> 400⛔️
[giza][2023-06-23 12:32:18.719] ⛔️Error message -> {'detail': 'Inactive user'}⛔️
```

Once activated you can successfully log into Giza:

```console
> giza users login

Enter your username 😎: gonmeso
Enter your password 🥷 :
[giza][2023-07-12 10:52:25.199] Log into Giza
[giza][2023-07-12 10:52:46.998] Credentials written to: /Users/gonmeso/.giza/.credentials.json
[giza][2023-07-12 10:52:47.000] Successfully logged into Giza ✅
```

If you want force the renewal of the token you can use `--renew` to force the log in. If the flag is not present we verify if there has been a previous log in and check that the token it's still valid.

```console
> giza users login

Enter your username 😎: gonmeso
Enter your password 🥷 :
[giza][2023-07-12 10:55:26.219] Log into Giza
[giza][2023-07-12 10:55:26.224] Token it still valid, re-using it from ~/.giza
[giza][2023-07-12 10:55:26.224] Successfully logged into Giza ✅
```

With `--renew`:

```console
> giza users login --renew

Enter your username 😎: gonmeso
Enter your password 🥷 :
[giza][2023-07-12 10:56:44.316] Log into Giza
[giza][2023-07-12 10:56:44.979] Credentials written to: /Users/gonmeso/.giza/.credentials.json
[giza][2023-07-12 10:56:44.980] Successfully logged into Giza ✅
```

**Note**: `--debug` its also available.

### Create API Key

Create an API key for the current user. This API key will be stored and will be used to authenticate the user in the future.

**You need te have an active account to log in**

```console
> giza users create-api-key
[giza][2024-01-17 15:27:27.936] Creating API Key ✅ 
[giza][2024-01-17 15:27:53.605] API Key written to: /Users/gizabrain/.giza/.api_key.json
[giza][2024-01-17 15:27:53.606] Successfully created API Key. It will be used for future requests ✅ 
```

Now you can use the API key to authenticate yourself withouth the need of login again and again.

**NOTE: The usage of API key is less secure than JWT, so use it with caution.**

### Me

Retrieve information about the current user.

**You need te have an active account**

```console
> giza users me

[giza][2023-07-12 10:59:43.821] Retrieving information about me!
[giza][2023-07-12 10:59:43.823] Token it still valid, re-using it from ~/.giza
{
  "username": "gonmeso",
  "email": "gonzalo@gizatech.xyz",
  "is_active": true
}
```

**Note**: `--debug` its also available.
