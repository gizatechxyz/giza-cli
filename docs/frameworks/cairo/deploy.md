# Deploy

To deploy a model, you must first have a version of that model. If you have not yet created a version, please refer to the [versions](../../resources/versions.md) documentation.

To create a new service, users can employ the `deploy` command. This command facilitates the deployment of a machine learning service ready to accept predictions at the `/cairo_run` endpoint, providing a straightforward method for deploying and using machine learning capabilities

```
> giza deployments deploy --model-id 1 --version-id 1 model.sierra
▰▰▰▰▰▱▱ Creating deployment!
[giza][2024-02-07 12:31:02.498] Deployment is successful ✅
[giza][2024-02-07 12:31:02.501] Deployment created with id -> 1 ✅
[giza][2024-02-07 12:31:02.502] Deployment created with endpoint URL: https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app 🎉
```

If a model is fully compatible the sierra file is not needed and can be deployed without using it in the command:

```
> giza deployments deploy --model-id 1 --version-id 1
▰▰▰▰▰▱▱ Creating deployment!
[giza][2024-02-07 12:31:02.498] Deployment is successful ✅
[giza][2024-02-07 12:31:02.501] Deployment created with id -> 1 ✅
[giza][2024-02-07 12:31:02.502] Deployment created with endpoint URL: https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app 🎉
```

{% hint style="danger" %}
For a partially compatible model, the sierra file must be provided, if not an error will be shown.
{% endhint %}

### Example request

Now our service is ready to accept predictions at the provided endpoint URL. To test this, we can use the `curl` command to send a POST request to the endpoint with a sample input.

```
> curl -X POST https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app/cairo_run \
     -H "Content-Type: application/json" \
     -d '{
           "args": "[2 2] [1 2 3 4]"
         }' | jq
{
  "result": [0.1234],
  "request_id": "b14bfbcf250b404192765d9be0811c9b"
}
```

There is an extra args, `job_size`, that can be used in each request to specify the size of the proving job so it has more CPU and memory available to generate the proof. An example:

```
> curl -X POST https://deployment-gizabrain-38-1-53427f44-dagsgas-ew.a.run.app/cairo_run \
     -H "Content-Type: application/json" \
     -d '{
           "args": "[2 2] [1 2 3 4]",
           "job_size": "M"
         }'
```

Available sizes are `S`, `M`, `L,` and `XL`, each with different usage limits.

## Download the proof

We can download the proof using the `download-proof` command available for the deployments:&#x20;

<pre class="language-sh"><code class="lang-sh"><strong>❯ giza deployments download-proof --model-id 1 --version-id 1 --deployment-id 1 --proof-id "b14bfbcf250b404192765d9be0811c9b"
</strong>[giza][2024-02-20 15:40:48.560] Getting proof from deployment 1 ✅
[giza][2024-02-20 15:40:49.288] Proof downloaded to zk.proof ✅
</code></pre>

The `proof id` used is the `request_id` returned in the response.
