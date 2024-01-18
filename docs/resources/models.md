# Models

Handle your models at Giza!

In Giza, a model represents a container for versions of your machine learning model. This design allows you to iterate and improve your ML model by creating new versions for it. Each model can have multiple versions, providing a robust and flexible way to manage the evolution of your ML models. This traceability feature ensures that you have a clear record of the original `onnx` model used for transpilation, who performed the transpilation, and the output generated.

Remember, you need to be logged in to use these functionalities!

## Create a Model

Creating a new model in Giza is a straightforward process. You only need to provide a name for the model using the `--name` option. However, you can also add a description of the model using the `--description` option. This can be helpful for keeping track of different models and their purposes.

Here's how you can do it:

```console
> giza models create --name my_new_model --description "A New Model"
[giza][2023-09-13 13:24:28.223] Creating model ✅ 
{
  "id": 1,
  "name": "my_new_model",
  "description": "A New Model"
}
```

Typically, the `transpile` command is used to handle model creation. During this process, the filename is checked for an existing model. If none is found, a new model is automatically created. However, manual creation of a model is also supported. For more information, refer to the transpile documentation ([cairo](../frameworks/cairo/transpile.md) and [ezkl](../frameworks/ezkl/transpile.md)).

## List Models

Giza provides a simple and efficient way to list all the models you have stored on the server. This feature is especially useful when you have multiple models and need to manage them effectively.

To list all your models, you can use the `list` command. This command retrieves and displays a list of all models stored in the server. Each model's information is printed in a json format for easy readability and further processing.

Here's how you can do it:

```console
> giza models list
[giza][2023-09-13 13:11:39.403] Listing models ✅ 
[
  {
    "id": 1,
    "name": "my_new_model",
    "description": "A New Model"
  },
  {
    "id": 2,
    "name": "Test",
    "description": "A Model for testing different models"
  }
]
```

## Retrieve Model Information

You can retrieve detailed information about a model stored on the server using its unique model id. This includes its name, description, and other id:

```console
> giza models get --model-id 1  # When we create model for you we output it in the logs so be aware
[giza][2023-09-13 13:17:53.594] Retrieving model information ✅ 
{
  "id": 1,
  "name": "my_new_model",
  "description": "A New Model"
}
```

Now we can see that we have a model successfully transpiled! Now if we want we could download it again!

## Download a successfully transpiled model

For this we can use the `download` command available in the CLI which only needs a `model_id` to download it again!

```console
> giza models download 1
[giza][2023-08-04 10:33:14.271] Transpilation is ready, downloading! ✅
[giza][2023-08-04 10:33:15.134] Transpilation saved at: cairo_model
```

Let's check the downloaded model:

```console
> tree cairo_model/
cairo_model/
├── cairo_project.toml
├── scarb.toml
└── src
    ├── graph.cairo
    ├── lib.cairo
    ├── weights
    │   ├── conv1_Conv_quant.cairo
    │   ├── conv2_Conv_quant.cairo
    │   ├── fc1_Gemm_MatMul_quant.cairo
    │   └── fc2_Gemm_MatMul_quant.cairo
    └── weights.cairo
```

## How do we transpile a model

Transpiling a model in Giza can be done in three ways, each designed to provide flexibility and ease of use. Here's how you can do it:

1. **Using the `giza transpile` command:** This command handles everything for you, from model creation to transpilation. It checks for an existing model and if none is found, a new model is automatically created and transpiled.

2. **Manually creating a model and then transpiling it:** This method involves two steps. First, you manually create a model using the `giza models create` command. Then, you transpile the model using the `giza transpile --model-id ...` or `giza versions transpile --model-id` command. This method gives you more control over the model creation and transpilation process.

3. **Using a previous model:** If you have a previously created model, you can transpile it by indicating the model-id in the `giza transpile --model-id ...` or `giza versions transpile --model-id` command. This method is useful when you want to create a new version of an existing model.

*Note: remember to use the `--framework` flag to indicate which one to use. It defaults to Cairo*

Remember, the choice of method depends on your specific needs and workflow. Giza provides these options to ensure that you can work with your models in the most efficient way possible.

For more information, refer to the transpile documentation ([cairo](../frameworks/cairo/transpile.md) and [ezkl](../frameworks/ezkl/transpile.md)).
