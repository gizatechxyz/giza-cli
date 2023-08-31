# Models

Handle your models at Giza!

Whenever we transpile a model under the hood we are creating a model, this models acts as a reference of the original `onnx` model that we used so we have traceability of who transpiled a model, which model was used and the output generated.

As always we need to be logged in to use its functionalities!

## Retrieve model information

We can retrieve information about a model that we have created (through a transpilation) and check its status and metadata:

```console
> giza models get 1  # This number is the model_id, check the output of a transpilation!
[giza][2023-08-04 10:29:07.198] Retrieving model information ✅ 
{
  "id": 1,
  "size": 52633,
  "name": "mv13.onnx",
  "status": "COMPLETED",
  "message": "Transpilation Successful!"
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

## Transpile a model (again)

Currently there are two ways in the CLI to transpile a model, the easy one is to directly use the `transpile` command which in reality is a shortcut to `giza models transpile ...` which is our second way.

Basically using `giza transpile ...` and `giza models transpile ...` will yield identical results as they perform the exact same operation!

```console
> giza transpile MNIST_quant.onnx --output-path my_awesome_model

[giza][2023-06-23 12:39:01.587] Reading model from path: MNIST_quant.onnx
[giza][2023-06-23 12:39:01.588] Sending model for transpilation
[giza][2023-06-23 12:39:04.657] Transpilation recieved!✅
[giza][2023-06-23 12:39:04.670] Trasnpilation saved at: my_awesome_model
```

This is equal to:

```console
> giza models transpile MNIST_quant.onnx --output-path my_awesome_model

[giza][2023-06-23 12:39:01.587] Reading model from path: MNIST_quant.onnx
[giza][2023-06-23 12:39:01.588] Sending model for transpilation
[giza][2023-06-23 12:39:04.657] Transpilation recieved!✅
[giza][2023-06-23 12:39:04.670] Trasnpilation saved at: my_awesome_model
```

More information about transpilation at [docs](transpile.md).