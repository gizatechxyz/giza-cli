# Verify

We have created a Proof of our EZKL version, now it's time to verify it!

As we already have the proof we can use the `verify` command to verify it, using the `--proof-id` option we can specify the proof that we want to verify.

As we are using a managed `version` we need to specify `--model-id` and `--version-id` to indicate which version we want to verify, so we can retrieve the generated files in the `setup` process (`giza transpile`).

```console
> giza verify -f EZKL --model-id 1 --version-id 1 --proof-id 1 --size S
[giza][2023-12-04 19:43:37.686] Verification job created with name 'verify-ezkl-20231204-32f44715' and id -> 1 ✅
[giza][2023-12-04 19:45:18.683] Verification job is successful ✅
```

If the job is successful that means that the proof is valid! Otherwise we will get an error message.
