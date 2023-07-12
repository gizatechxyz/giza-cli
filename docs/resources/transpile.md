# Transpile

Perform the transpilation of an ONNX model to a cairo model powered by [✨Orion✨](https://github.com/gizatechxyz/orion)

Gets the model in the specified path and send it for transpilation. This will output the model to `cairo_model/` folder by default but can be changed by using `--output-path`.

```console
> giza transpile MNIST_quant.onnx --output-path my_awesome_model

[giza][2023-06-23 12:39:01.587] Reading model from path: MNIST_quant.onnx
[giza][2023-06-23 12:39:01.588] Sending model for transpilation
[giza][2023-06-23 12:39:04.657] Transpilation recieved!✅
[giza][2023-06-23 12:39:04.670] Trasnpilation saved at: my_awesome_model
```

The result will be saved at the provided path `my_awesome_model/`.

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

This command can be used multiple times with different models to transpile. For transpiling new versions of a model make sure to change the name as of now model names must be unique per user.

**Note**: `--debug` its also available.
