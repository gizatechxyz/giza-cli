# How To Create a Proof Using Giza CLI

After transpiling the model to Cairo using Giza CLI, the next step is to create a proof. This proof is a cryptographic evidence that the computation (inference) was done correctly without revealing any information about the data or the computation itself.

## Prerequisites

We need to install the following tools:

* [Giza CLI](cli.gizatech.xyz)
* [Rust](https://www.rust-lang.org/tools/install)
* [Scarb](https://docs.swmansion.com/scarb/)
* [`starknet-sierra-compile`](https://github.com/starkware-libs/cairo/tree/main/crates/bin/starknet-sierra-compile)

## Embed the model into a Starknet Contract

First, we need to compile the Cairo contract to a Starknet Contract, more information about starknet contracts [here](https://book.cairo-lang.org/ch99-00-starknet-smart-contracts.html). For now we don't need to dive deep into how these contracts work, as currently we need to make it a contract due a temporary limitation in the prover, once this is solved we should be able to generate the proof without the need of a contract.

Add the `starknet` as a dependency in the `Scarb.toml` file:

```toml
[dependencies]
starknet = "2.0.2"
orion = { git = "https://github.com/gizatechxyz/orion.git" }

# ...

[[target.starknet-contract]]
```

Then declare our program as a contract:

```rust
// inference.cairo
// Create a module and declare it as a contract
#[starknet::contract]
mod OrionRunner {

    // Kepp your imports as declared previously
    // use ...

    // Declare the contract storage, in this case is a dummy storage as we won't use it
	#[storage]
	struct Storage { 
		id: u8,
	}

    // Declare the main function as an external function and add `self: @ContractState` as the first argument
	#[external(v0)]
	fn main(self: @ContractState){
		// The models code goes here
	}
// Remember to close the module bracket!
}
```

## Compile the contract

This is done using the `scarb build` command with the main objective of creating the `sierra.json` file that will be used to generate the proof. These files will be generated in the `target/dev` folder.

```console
❯ scarb build
    Updating git repository https://github.com/gizatechxyz/orion
    Updating git repository https://github.com/keep-starknet-strange/alexandria
    Updating git repository https://github.com/influenceth/cubit
   Compiling mnist_pytorch v0.1.0 (/Users/gizabrain/src/giza/giza-cli/examples/mnist/mnist_cairo/Scarb.toml)
    Finished release target(s) in 7 seconds
```

Now this will create two files, but we are only interested in one of them, the `{{project name}}_OrionRunner.sierra.json` file.

## Convert the `sierra.json` file to `casm.json`

For this step we need the `starknet-sierra-compile` tool, this tool will convert the `sierra.json` file to a `casm.json`. If you don't already have it, to get it you need to get it from the Cairo repository and build it:

```bash
git clone git@github.com:starkware-libs/cairo.git
cd cairo
cargo build
```

Then the binary will be placed at `target/debug/starknet-sierra-compile`. Now we can use it to convert the file:

```bash
starknet-sierra-compile -- target/dev/{{project_name}}_OrionRunner.sierra.json output.casm.json
```

## Generate the proof

Finally, we can generate the proof using the `giza prove` command:

```console
❯ giza prove --size M output.casm.json
[giza][2023-10-26 13:29:22.337] Proving job created with name 'proof-job-20231026-73fb1007' and id -> 1 ✅
# This log live updates with the job elapsed time
[giza][2023-10-26 13:32:44.431] Job status is 'PROCESSING', elapsed 103.0s
# Once finished it will update to indicate that the job finished
[giza][2023-10-26 13:37:06.634] Proving job is successful ✅
[giza][2023-10-26 13:37:06.748] Proof metrics:
{
  "cairovm_execution_time": 4.973674,
  "proving_time": 316.3519
}
[giza][2023-10-26 13:37:07.471] Proof saved at: zk.proof
```

And now we have our proof!

Note: The `verify` command is coming soon!

