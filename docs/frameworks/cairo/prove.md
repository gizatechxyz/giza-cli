# Prove

Giza provides two methods for proving Orion Cairo programs: through the CLI or directly after running inference on the Giza Platform. Below are detailed instructions for both methods

## Option 1: Prove a Model After Running Inference

**Deploying Your Model**

After deploying your model on the Giza Platform, you will receive a URL for your deployed model. Refer to the [Endpoints section](../../resources/endpoints.md) for more details on deploying models.

**Running Inference**

To run inference, use the `/cairo_run` endpoint of your deployed model's URL. For example:

```
https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app/cairo_run
```

This action will execute the inference, generate Trace and Memory files on the platform, and initiate a proving job. The inference process will return the output result along with a request ID.

**Checking Proof Status**

To check the status of your proof, use the following command:

```
giza endpoints get-proof --model-id <MODEL_ID> --version-id <VERSION_ID> --endpoint-id <ENDPOINT_ID> --proof-id <REQUEST_ID>
```

**Downloading Your Proof**

Once the proof is ready, you can download it using:

```
giza endpoints download-proof --model-id <MODEL_ID> --version-id <VERSION_ID> --endpoint-id <ENDPOINT_ID> --proof-id <REQUEST_ID> --output-path <OUTPUT_PATH>
```

{% hint style="info" %}
You can find an extensive example in [Giza Action tutorial](https://actions.gizatech.xyz/tutorials/build-a-verifiable-neural-network-with-giza-actions#run-and-prove)
{% endhint %}

## Option 2: Proving a Model Directly from the CLI

Alternatively, you can prove a model directly using the CLI without deploying the model for inference. This method requires providing Trace and Memory files, which can only be obtained by running [CairoVM](https://github.com/lambdaclass/cairo-vm) in proof mode.

**Running the Prove Command**

Execute the following command to prove your model:

```
giza prove --trace <TRACE_PATH> --memory <MEMORY_PATH> --output-path <OUTPUT_PATH>
```

{% hint style="info" %}
This option is less preferred due to the necessity of dealing with CairoVM.
{% endhint %}

{% hint style="danger" %}
If you opt for this method, ensure you use the following commit of CairoVM: `1a78237`.
{% endhint %}
