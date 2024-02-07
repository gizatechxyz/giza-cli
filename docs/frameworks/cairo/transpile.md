# Transpile

Transpilation is a crucial process in the deployment of Verifiable Machine Learning models. It involves the transformation of an ONNX model into a Cairo model. These models can generate proofs that can be verified, ensuring the integrity and reliability of the model's predictions.

The transpilation of an ONNX model to a Cairo model is powered by [✨Orion✨](https://github.com/gizatechxyz/orion)

The transpilation process begins by reading the model from the specified path. The model is then sent for transpilation. By default, the output of this process is saved in the `cairo_model/` folder. However, you can specify a different output path using the `--output-path` option.

```console
> giza transpile awesome_model.onnx --output-path my_awesome_model
[giza][2023-09-13 12:56:43.725] No model id provided, checking if model exists ✅ 
[giza][2023-09-13 12:56:43.726] Model name is: awesome_model
[giza][2023-09-13 12:56:43.978] Model Created with id -> 1! ✅
[giza][2023-09-13 12:56:44.568] Sending model for transpilation ✅ 
[giza][2023-09-13 12:56:55.577] Transpilation recieved! ✅
[giza][2023-09-13 12:56:55.583] Transpilation saved at: cairo_model
```

The result of the transpilation process is saved at the provided path, in this case, `my_awesome_model/`.

```console
> tree my_awesome_model/
my_awesome_model
├── inference
│   ├── Scarb.toml
│   └── src
│       └── lib.cairo
└── initializers
    ├── node_l1
    │   ├── Scarb.toml
    │   └── src
    │       └── lib.cairo
```

## Supported Operators

| Operator |      Implemented     |
| :------: | :------------------: |
|    Abs   | :white\_check\_mark: |
|   Acos   | :white\_check\_mark: |
|   Acosh  | :white\_check\_mark: |
|    Add   | :white\_check\_mark: |
|    And   | :white\_check\_mark: |
|    Div   | :white\_check\_mark: |
|    Mul   | :white\_check\_mark: |
|    Sub   | :white\_check\_mark: |
|  Argmax  | :white\_check\_mark: |
|  Argmin  | :white\_check\_mark: |
|   Asin   | :white\_check\_mark: |
|   Asinh  | :white\_check\_mark: |
|   Atan   | :white\_check\_mark: |
|   Relu   | :white\_check\_mark: |
| Constant | :white\_check\_mark: |
|  MatMul  | :white\_check\_mark: |
|   Gemm   | :white\_check\_mark: |

## How do we transpile a model?

There are three main methods for transpiling a model:

### **Method 1: Using the `giza transpile` command**

```
 giza transpile awesome_model.onnx --output-path my_awesome_model
```

This is the simplest method and is recommended for most users.\
When you run this command, Giza handles everything for you:

* It first checks if a model with the specified name already exists. If not, it creates a new model and then transpiles it.
* The output of this process is saved in the `cairo_model/` folder by default, but you can specify a different output path using the `--output-path` option.

This is the strategy that we followed in the example before.

### **Method 2: Manually creating a model and then transpiling it**

This method gives you more control over the process.

1. First, you create a model manually using the `giza models create` command.
2. After the model is created, you can transpile it using the `giza transpile --model-id ...`&#x20;

This method is useful when you want to specify particular options or parameters during the model creation and transpilation process.

```console
> giza models create --name awesome_model --description "A Model for testing different models"
[giza][2023-09-13 14:04:59.532] Creating model ✅ 
{
  "id": 2,
  "name": "awesome_model",
  "description": "A Model for testing different models"
}
```

```console
> giza transpile --model-id 2 awesome_model.onnx --output-path new_awesome_model
[giza][2023-09-13 14:08:38.022] Model found with id -> 2! ✅
[giza][2023-09-13 14:08:38.712] Sending model for transpilation ✅ 
[giza][2023-09-13 14:08:49.879] Transpilation recieved! ✅
[giza][2023-09-13 14:08:49.885] Transpilation saved at: new_awesome_model
```

### **Method 3: Using a previous model**

If you have a previously created model, you can transpile it by indicating the model-id in the `giza transpile --model-id ...` or `giza versions transpile --model-id` command.

* This method is useful when you want to create a new version of an existing model.
* The output of the transpilation process is saved in the same location as the original model.

```console
# Using the previous model (id: 2) we can transpile a new model, which will create version 2 of the model.
giza transpile --model-id 29 awesome_model.onnx --output-path new_awesome_model
[giza][2023-09-13 14:11:30.015] Model found with id -> 2! ✅
[giza][2023-09-13 14:11:30.541] Sending model for transpilation ✅ 
[giza][2023-09-13 14:11:41.601] Transpilation recieved! ✅
[giza][2023-09-13 14:11:41.609] Transpilation saved at: new_awesome_model
```

## What is happening with the models and versions?

In Giza, a model is essentially a container for versions. Each version represents a transpilation of a machine learning model at a specific point in time. This allows you to keep track of different versions of your model as it evolves and improves over time.

To check the current models and versions that have been created, you can use the following steps:

1. Use the `giza models list` command to list all the models that have been created.
2. For each model, you can use the `giza versions list --model-id ...` command to list all the versions of that model.

Remember, each version represents a specific transpilation of the model. So, if you have made changes to your machine learning model and transpiled it again, it will create a new version.

This system of models and versions allows you to manage and keep track of the evolution of your machine learning models over time.

For example, let's say you have created a model called `awesome_model` and transpiled it twice. This will create two versions of the model, version 1 and version 2. You can check the status of these versions using the `giza versions list --model-id ...` command.

```console
giza versions list --model-id 29
[giza][2023-09-13 14:17:08.006] Listing versions for the model ✅ 
[
  {
    "version": 1,
    "size": 52735,
    "status": "COMPLETED",
    "message": "Transpilation Successful!",
    "description": "Initial version",
    "created_date": "2023-09-13T12:08:38.177605",
    "last_update": "2023-09-13T12:08:43.986137"
  },
  {
    "version": 2,
    "size": 52735,
    "status": "COMPLETED",
    "message": "Transpilation Successful!",
    "description": "Initial version",
    "created_date": "2023-09-13T12:11:30.165440",
    "last_update": "2023-09-13T12:11:31.625834"
  }
]
```
