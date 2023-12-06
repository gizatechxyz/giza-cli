# Prove

Time to create a Proof of our Cairo program!

Once we have our `json` we can use the `prove` command to create our proof!

Basically, this command will create a proving job at Giza and once the job is completed we will download the created proof.

```console
> giza prove orion_runner.casm.json --size M
[giza][2023-08-04 11:30:36.892] Proving job created with name 'proof-job-20230804-2d3d857a' and id -> 1 ✅
[giza][2023-08-04 11:37:41.848] Proving job is successful ✅  # This output will be updated live!
[giza][2023-08-04 11:37:42.097] Proof Cairo VM execution time -> 5.2519965
[giza][2023-08-04 11:37:42.099] Proof proving time -> 310.86398
[giza][2023-08-04 11:37:43.007] Proof saved at: zk.proof
```

As we can see the job takes some time, and because of this we are actively waiting for the job to be completed, once it's done all information and the proof are retrieved.