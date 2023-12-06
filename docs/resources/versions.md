# Versions

Manage your model versions at Giza!

In Giza, a version represents a specific iteration of your machine learning model within a Giza Model. This design allows you to iterate and improve your ML model by creating new versions for it. Each model can have multiple versions, providing a robust and flexible way to manage the evolution of your ML models. This traceability feature ensures that you have a clear record of each version of your model.

Remember, you need to be logged in to use these functionalities!

## Retrieve Version Information

You can retrieve detailed information about a specific version of a model using its unique model ID and version ID. This includes its version number, size, description, status, creation date, and last update date.

Here's how you can do it:

```console
> giza versions get --model-id 1 --version-id 1
[giza][2023-09-13 14:38:30.965] Retrieving version information ✅ 
{
  "version": 1,
  "size": 52735,
  "status": "COMPLETED",
  "message": "Transpilation Successful",
  "description": "Initial version of the model",
  "created_date": "2023-07-04T11:15:09.448709",
  "last_update": "2023-08-25T11:08:51.815545"
}
```

## List Versions

Giza provides a simple and efficient way to list all the versions of a specific model you have. This feature is especially useful when you have multiple versions of a model and need to manage them effectively.

To list all your versions of a model, you can use the list command. Each version's information is printed in a json format for easy readability and further processing.

Here's how you can do it:

```console
> giza versions list --model-id 1
[giza][2023-09-13 14:41:09.209] Listing versions for the model ✅ 
[
  {
    "version": 1,
    "size": 52735,
    "status": "COMPLETED",
    "message": "Transpilation Successful",
    "description": "Initial version of the model",
    "created_date": "2023-07-04T11:15:09.448709",
    "last_update": "2023-08-25T11:08:51.815545"
  },
  {
    "version": 2,
    "size": 52735,
    "status": "COMPLETED",
    "message": "Transpilation Successful!",
    "description": "Intial version",
    "created_date": "2023-09-13T10:24:20.018476",
    "last_update": "2023-09-13T10:24:24.376009"
  }
]
```

## Transpile a Model Version

**Note:** This has been explained previously in the transpile documentation ([cairo](../frameworks/cairo/transpile.md) and [ezkl](../frameworks/ezkl/transpile.md)).

Transpiling a model version in Giza is a crucial step in the model deployment process. Transpilation is the process of converting your machine learning model into a format that can be executed on Giza. This process involves converting the model into a series of Cairo instructions or performing the setup using `ezkl`.

When you transpile a model, you're essentially creating a new version of that model. Each version represents a specific iteration of your machine learning model, allowing you to track and manage the evolution of your models effectively.

Here's how you can transpile a model version:

```console
> giza versions transpile --framework CAIRO awesome_model.onnx --output-path my_awesome_model
[giza][2023-09-13 12:56:43.725] No model id provided, checking if model exists ✅ 
[giza][2023-09-13 12:56:43.726] Model name is: awesome_model
[giza][2023-09-13 12:56:43.978] Model Created with id -> 1! ✅
[giza][2023-09-13 12:56:44.568] Sending model for transpilation ✅ 
[giza][2023-09-13 12:56:55.577] Transpilation recieved! ✅
[giza][2023-09-13 12:56:55.583] Transpilation saved at: cairo_model
```

Once the transpilation process is complete, a new version of the model is created in Giza. The version will be downloaded and saved at the specified output path, but you can also execute later the `download` command to download it again.

## Download a Successfully Transpiled Version

Once a model has been successfully transpiled, it's not necessary to go through the transpilation process again. The transpiled version is stored and can be downloaded anytime you need it. This is done using the download command in the CLI. This command specifically requires the model_id and version_id to accurately identify and download the correct transpiled version. This feature saves time and computational resources, making the management of your models more efficient.

*Note: currently is only available for the Cairo framework*

```console
> giza versions download --model-id 1 --version-id 1 --output-path path
[giza][2023-08-04 10:33:14.271] Transpilation is ready, downloading! ✅
[giza][2023-08-04 10:33:15.134] Transpilation saved at: path
```

Let's check the downloaded version:

```console
> tree path/
path/
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

For more information on how to transpile a model, refer to the transpile documentation ([cairo](../frameworks/cairo/transpile.md) and [ezkl](../frameworks/ezkl/transpile.md)).
