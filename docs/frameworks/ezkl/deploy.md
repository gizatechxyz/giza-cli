# Deploy

To deploy a model, you must first have a version of that model. If you have not yet created a version, please refer to the [versions](../../resources/versions.md) documentation.

To create a new service, users can employ the `deploy` command. This command facilitates the deployment of a machine learning service ready to accept predictions at the `/predict` endpoint, providing a straightforward method for deploying and using machine learning capabilities as an API endpoint. As we are using `EZKL` we need to add `--framework EZKL` (or `-f EZKL` for short) to the command:

{% code overflow="wrap" %}
```shell
> giza endpoints deploy --model-id 1 --version-id 1 --framework EZKL
▰▰▰▰▰▱▱ Creating endpoint!
[giza][2024-02-07 12:31:02.498] Endpoint is successful ✅
[giza][2024-02-07 12:31:02.501] Endpoint created with id -> 1 ✅
[giza][2024-02-07 12:31:02.502] Endpoint created with endpoint URL: https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app 🎉
```
{% endcode %}

## Example Request

Now the model is available to generate predictions and generate proofs of those predictions. The schema of the data is the same as used to create the `input.json` needed to create version, for a linear regression it would be:

```json
{
  "input_data": [
    [
      0.12177091836929321,
      0.7048522233963013
    ]
  ]
}
```

To execute a prediction using **cURL**:

```sh
curl https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app/predict \
-H "Content-Type: application/json" -d '{
    "input_data": [
    [
      0.12177091836929321,
      0.7048522233963013
    ]
  ]
}' | jq
```

This yields the following response:

```json
{
  "prediction": [
    [
      4.53125
    ]
  ],
  "request_id": "d0564505755944b8bef9292d980f3e27"
}
```

There is an extra args, `job_size`, that can be used in each request to specify the size of the proving job so it has more CPU and memory available to generate the proof. An example:

```sh
curl https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app/predict \
-H "Content-Type: application/json" -d '{
    "input_data": [
    [
      0.12177091836929321,
      0.7048522233963013
    ]
  ],
  "job_size": "M"
}' | jq
```

Available sizes are `S`, `M`, `L,` and `XL`, each with different usage limits.

## Download the proof

We can download the proof using the `download-proof` command available for the endpoints:&#x20;

<pre class="language-sh"><code class="lang-sh"><strong>❯ giza endpoints download-proof --model-id 1 --version-id 1 --endpoint-id 1 --proof-id "d0564505755944b8bef9292d980f3e27"
</strong>[giza][2024-02-20 15:40:48.560] Getting proof from endpoint 1 ✅
[giza][2024-02-20 15:40:49.288] Proof downloaded to zk.proof ✅
</code></pre>

The `proof id` used is the `request_id` returned in the response.
