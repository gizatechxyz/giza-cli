# Frameworks

Giza operates on multiple frameworks simultaneously. This allows you to switch between frameworks as needed, providing flexibility and control over your development process.

## Cairo

Cairo is a framework for creating and executing programs that use zero-knowledge proofs to verify computations off-chain. It is designed to be highly expressive, allowing developers to write programs that are both complex and efficient.

## EZKL

`ezkl` is an engine for doing inference for deep learning models and other computational graphs in a zk-snark using `halo2` as the backend. For more information about `ezkl`, see the [ezkl repository](https://github.com/zkonduit/ezkl)

## Switching between frameworks

As we aim to bring the best of both worlds to developers, Giza allows us to perform the same operations on both frameworks just with a single change in the command line, the `--framework` flag.

This flag allows you to specify which framework you want to use for the current operation but the underlying work that we do is the same.

For example, if you want to use the Cairo framework, you would use the `--framework CAIRO` flag. Similarly, for the EZKL framework, you would use the `--framework EZKL` flag.

For example, if you want to transpile a program using the Cairo framework, you would use the following command:

```bash
giza transpile --framework CAIRO model.onnx
```

Similarly, if you want to transpile a program using the EZKL framework, you would use the following command:

```bash
giza transpile --framework EZKL --input-data input.json model.onnx
```

The `transpile` command in EZKL is essentially the same as the `setup()` command used to perform the trusted setup, as we need extra information to perform the `setup` it has an additional `--input-data` flag that allows you to specify the input data for the model.

This allows you to switch between frameworks as needed, providing flexibility and control over your development process.

For more information about the available commands for each framework, please refer to the [Cairo](/docs/frameworks/cairo.md) and [EZKL](/docs/frameworks/ezkl.md) documentation.
