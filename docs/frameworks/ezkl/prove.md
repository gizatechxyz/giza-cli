# Prove

{% hint style="danger" %}
Currently, any related EZKL capabilities are disabled
{% endhint %}

Time to create a Proof of our EZKL version!

Once we have the input data that we want to use we can use the `prove` command to create our proof!

This command will create a proving job at Giza and once the job is completed we will download the created proof.

```console
> giza prove --framework EZKL --model-id 1 --version-id 1 --size M input.json
[giza][2023-12-04 19:41:55.236] Proving job created with name 'proof-ezkl-20231204-33e59441' and id -> 1 ✅
[giza][2023-12-04 19:43:36.337] Proving job is successful ✅[giza][2023-12-04 19:43:36.447] Proof created with id -> 1 ✅
[giza][2023-12-04 19:43:36.448] Proof metrics:
{
  "proving_time": 12.2238187789917
}
[giza][2023-12-04 19:43:37.046] Proof saved at: zk.proof
```

As we can see the job takes some time, and because of this we are actively waiting for the job to be completed, once it's done all information and the proof are retrieved.

Now we can see that we have a proof successfully created! Now if we want we could verify it! Let's check the [verify](../frameworks/ezkl/verify.md) documentation to see how to do it!
