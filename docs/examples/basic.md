# Basic CLI Example

For this example we will create a user, retrieve information from it and transpile a model.

## Create User

This is the first step! We create the user and then we need to verify the account by checking the email.

```console
> giza users create

Enter your username 😎: my-username
Enter your password 🥷 : (this is a secret)
Enter your email 📧: gonzalo@gizatech.xyz
[giza][2023-06-23 12:29:40.543] Creating user in Giza Platform ✅
[giza][2023-06-23 12:29:41.417] User created ✅. Check for a verification email 📧
```

Then we need to verify the email. We just need to click on the buttom and we'll be redireted to the verification endpoint.

## Login

If it is not verified login will be disabled!

```console
> giza users login

Enter your username 😎: my-username
Enter your password 🥷 :
[giza][2023-06-23 12:32:17.917] Log into Giza Platform
[giza][2023-06-23 12:32:18.716] ⛔️Could not authorize the user⛔️
[giza][2023-06-23 12:32:18.718] ⛔️Status code -> 400⛔️
[giza][2023-06-23 12:32:18.719] ⛔️Error message -> {'detail': 'Inactive user'}⛔️
```

But once we verify the account we will be able to authenticate with the platform.

```console
> giza users login

Enter your username 😎: my-username
Enter your password 🥷 :
[giza][2023-06-23 12:34:33.576] Log into Giza Platform
[giza][2023-06-23 12:34:34.400] Successfully logged into Giza Platform ✅
```

## Retrieve user information

Now that we are authenticated we can connect with the platform!

```console
> giza users me

[giza][2023-06-23 12:35:33.287] Retrieving information about me!
{
  "username": "my-username",
  "email": "gonzalo@gizatech.xyz",
  "is_active": true
}
```

## Transpile a model

We have our `onnx` model and we want to transpile it, `giza` makes it easy by providing the command for it!

```console
> giza transpile MNIST_quant.onnx --output-path my_awesome_model

[giza][2023-06-23 12:39:01.587] Reading model from path: MNIST_quant.onnx
[giza][2023-06-23 12:39:01.588] Sending model for transpilation
[giza][2023-06-23 12:39:04.657] Transpilation recieved!✅
[giza][2023-06-23 12:39:04.670] Trasnpilation saved at: my_awesome_model
```

Let's check the result:

```console
> tree my_awesome_model

my_awesome_model
├── cairo_project.cairo
├── scarb.toml
└── src
    ├── conv1
    │   └── Conv_quant.cairo
    ├── conv1.cairo
    ├── conv2
    │   └── Conv_quant.cairo
    ├── conv2.cairo
    ├── fc1
    │   └── Gemm_MatMul_quant.cairo
    ├── fc1.cairo
    ├── fc2
    │   └── Gemm_MatMul_quant.cairo
    ├── fc2.cairo
    ├── graph.cairo
    └── lib.cairo
```
