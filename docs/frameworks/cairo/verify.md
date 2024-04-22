# Verify

After successfully creating a proof for your Orion Cairo model, the next step is to verify its validity. Giza offers two methods for proof verification: using the `proof-id` or directly specifying the proof file path.

## Option 1: Verify Using Proof-ID

To verify a proof by providing the `proof-id`, use the following command:

```
giza verify --model-id 1 --version-id 1 --proof-id 1 --size S
```

Upon successful submission, you will see a confirmation message indicating that the verification procces has begun. Once the verification process is complete, a success message will confirm the validity of the proof:

```
[giza][2024-04-22 13:48:12.236] Verifying proof...
[giza][2024-04-22 13:48:14.985] Verification result: True
[giza][2024-04-22 13:48:14.985] Verification time: 2.363822541
```

A `--use-remote` flag can be added to the command to verify the proof using a job. This flag is optional and its strongly discouraged as verification time is 10x slower than the default method.
```

## Option 2: Verify by Providing the Proof Path

Alternatively, you can verify a proof by specifying the path to the proof file directly. This option uses by default the `--use-job` flag to verify the proof using a job. To verify a proof using the proof file path, use the following command:

```
giza verify --proof /path/to/the/proof --size S
```

Similar to the first option, you will receive confirmation of the verification job creation followed by a success message upon completion:

```
[giza][2023-12-04 19:43:37.686] Verification job created with name 'verify-cairo-20231204-32f44715' and id -> 1 ✅
[giza][2023-12-04 19:45:18.683] Verification job is successful ✅
```

## Verification Outcome

If the verification job completes successfully, it indicates that the proof is valid. If there are any issues during the verification process, Giza will provide an error message detailing the problem.
