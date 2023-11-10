import json
import sys
import time
from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError
from rich import print_json
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

from giza import API_HOST
from giza.client import (
    JobsClient,
    ModelsClient,
    ProofsClient,
    VersionJobsClient,
    VersionsClient,
)
from giza.options import DEBUG_OPTION
from giza.schemas.jobs import Job, JobCreate
from giza.schemas.models import ModelCreate
from giza.schemas.proofs import Proof
from giza.schemas.versions import VersionCreate, VersionStatus, VersionUpdate
from giza.utils import Echo, get_response_info
from giza.utils.enums import Framework, JobKind, JobSize, JobStatus

app = typer.Typer()


@app.command(
    short_help="🔥 Sets up a model and creates the outputs, handled by Giza.",
    help="""🔥 This command sets up a model and creates the outputs, handled by Giza.
    It requires the path to the ONNX model and the ID of the model where a new version will be created.
    If the model ID is not provided, it will check if the model exists and use it if it does, or create a new one if it doesn't.
    It also requires the size of the job and the input data.
    If the model description is provided when the model ID is also provided, it will ignore the provided description.
    The command will then retrieve the model, create a version, send the model for setup, and create a setup job.
    It will keep checking the status of the job until it is completed or fails.
    If the job validation fails or there is an HTTP error, it will print an error message and exit the program.""",
)
def setup(
    model_path: str = typer.Argument(None, help="Path to the ONNX model"),
    model_id: int = typer.Option(
        None, help="The ID of the model where a new version will be created"
    ),
    desc: str = typer.Option(None, help="Description of the version"),
    model_desc: int = typer.Option(
        None, help="Description of the Model to create if model_id is not provided"
    ),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    input_data: str = typer.Option(None, "--input-data", "-i"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    This function executes the setup of the model and creates the outputs, handled by Giza.
    It first checks if the input data is provided. If not, it prints an error message and exits the program.
    If the model ID is not provided, it checks if the model exists and uses it if it does, or creates a new one if it doesn't.
    It then retrieves the model, creates a version, sends the model for setup, and creates a setup job.
    It keeps checking the status of the job until it is completed or fails.
    If the job validation fails or there is an HTTP error, it prints an error message and exits the program.
    """
    echo = Echo(debug=debug)
    if input_data is None:
        echo.error("Input data is required")
        sys.exit(1)
    if model_id is None:
        model_name = model_path.split("/")[-1].split(".")[0]
        echo("No model id provided, checking if model exists ✅ ")
        echo(f"Model name is: {model_name}")
    if model_desc is not None and model_id is not None:
        echo(
            "Model description is not required when model id is provided, ignoring provided description ✅ "
        )
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            model_task = progress.add_task(
                description="Retrieving Model...", total=None
            )
            echo.debug(f"Reading model from path: {model_path}")
            models_client = ModelsClient(API_HOST)
            if model_id is None:
                model = models_client.get_by_name(model_name)
                if model is not None:
                    echo("Model already exists, using existing model ✅ ")
                else:
                    model_create = ModelCreate(name=model_name, description=model_desc)
                    model = models_client.create(model_create)
                    echo(f"Model Created with id -> {model.id}! ✅")
            else:
                model = models_client.get(model_id)
                echo(f"Model found with id -> {model.id}! ✅")
            progress.update(model_task, completed=True, visible=False)
            version_task = progress.add_task(
                description="Creating Version...", total=None
            )
            client = VersionsClient(API_HOST)
            version_create = VersionCreate(
                description=desc if desc else "Intial version",
                size=Path(model_path).stat().st_size,
                framework=Framework.EZKL,
            )
            version, upload_url = client.create(
                model.id, version_create, model_path.split("/")[-1]
            )
            progress.update(version_task, completed=True, visible=False)
            echo("Sending model for setup ✅ ")
            with open(model_path, "rb") as f:
                client._upload(upload_url, f)
                echo.debug("Model Uploaded! ✅")

            client.update(
                model.id, version.version, VersionUpdate(status=VersionStatus.UPLOADED)
            )
        echo(f"Using model with id -> {model.id} and version -> {version.version} ✅")
        jobs_client = VersionJobsClient(API_HOST)
        with open(input_data) as casm:
            job: Job = jobs_client.create(
                model.id,
                version.version,
                JobCreate(size=size, framework=Framework.EZKL),
                casm,
            )
        echo(f"Setup job created with name '{job.job_name}' and id -> {job.id} ✅")
        with Live() as live:
            while True:
                current_job: Job = jobs_client.get(model.id, version.version, job.id)
                if current_job.status == JobStatus.COMPLETED:
                    live.update(echo.format_message("Setup job is successful ✅"))
                    break
                elif current_job.status == JobStatus.FAILED:
                    live.update(
                        echo.format_error(
                            f"Setup Job with name '{current_job.job_name}' and id {current_job.id} failed"
                        )
                    )
                    sys.exit(1)
                else:
                    live.update(
                        echo.format_message(
                            f"Job status is '{current_job.status}', elapsed {current_job.elapsed_time}s"
                        )
                    )
                    time.sleep(20)
    except ValidationError as e:
        echo.error("Job validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not create the job")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)


@app.command(
    short_help="🔥 Proves a specific EZKL model.",
    help="""🔥 Proves a specific EZKL model using the provided model id and version id.
    This will create a proving job and check the status, once it finishes if COMPLETED the proof is downloaded at the output path
    The daily jobs allowed are rate limited by the backend.
    """,
)
def prove(
    model_id: Optional[int] = typer.Option(
        None, "--model-id", "-m", help="The ID of the model to prove"
    ),
    version_id: Optional[int] = typer.Option(
        None, "--version-id", "-v", help="The version ID of the model to prove"
    ),
    input_data: str = typer.Option(None, "--input-data", "-i"),
    output_path: str = typer.Option(
        "proof.ezkl", "--output-path", "-o", help="The output path for the proof"
    ),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    echo = Echo(debug=debug)
    if model_id is None or version_id is None or input_data is None:
        echo.error("model_id, version_id, and input_data are all required")
        sys.exit(1)
    try:
        client = JobsClient(API_HOST)
        with open(input_data) as data:
            job: Job = client.create(
                JobCreate(
                    size=size,
                    framework=Framework.EZKL,
                    kind=JobKind.PROOF,
                    model_id=model_id,
                    version_id=version_id,
                ),
                data,
            )
        echo(f"Proving job created with name '{job.job_name}' and id -> {job.id} ✅")
        with Live() as live:
            while True:
                current_job: Job = client.get(job.id)
                if current_job.status == JobStatus.COMPLETED:
                    live.update(echo.format_message("Proving job is successful ✅"))
                    break
                elif current_job.status == JobStatus.FAILED:
                    live.update(
                        echo.format_error(
                            f"Proving Job with name '{current_job.job_name}' and id {current_job.id} failed"
                        )
                    )
                    sys.exit(1)
                else:
                    live.update(
                        echo.format_message(
                            f"Job status is '{current_job.status}', elapsed {current_job.elapsed_time}s"
                        )
                    )
                    time.sleep(20)
        with open(output_path, "wb") as f:
            proof_client = ProofsClient(API_HOST)
            proof: Proof = proof_client.get_by_job_id(current_job.id)
            echo("Proof metrics:")
            print_json(json.dumps(proof.metrics))
            f.write(proof_client.download(proof.id))
            echo(f"Proof saved at: {output_path}")
    except ValidationError as e:
        echo.error("Job validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not create the job")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)


@app.command()
def verify(
    proof_id: Optional[int] = typer.Option(
        None, "--proof-id", "-p", help="The id of the proof to verify"
    ),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    model_id: Optional[int] = typer.Option(
        None, "--model-id", "-m", help="The ID of the model to prove"
    ),
    version_id: Optional[int] = typer.Option(
        None, "--version-id", "-v", help="The version ID of the model to prove"
    ),
    proof: str = typer.Option(None, "--input-data", "-i"),
    debug: bool = DEBUG_OPTION,
):
    """
    Create a verification job.
    This command will create a verification job with the provided proof id.
    The job size, model id, and version id can be optionally specified.
    """
    echo = Echo()
    if not model_id or not version_id:
        echo.error("Both model id and version id must be provided.")
        sys.exit(1)
    if proof_id and proof:
        echo.error("You can only use either proof_id or proof, but not both.")
        sys.exit(1)
    try:
        job: Job
        client = JobsClient(API_HOST)
        if proof_id:
            job = client.create(
                JobCreate(
                    size=size,
                    framework=Framework.EZKL,
                    kind=JobKind.VERIFY,
                    model_id=model_id,
                    version_id=version_id,
                    proof_id=proof_id,
                ),
                None,
            )
        elif proof:
            with open(proof) as data:
                job = client.create(
                    JobCreate(
                        size=size,
                        framework=Framework.EZKL,
                        kind=JobKind.VERIFY,
                        model_id=model_id,
                        version_id=version_id,
                    ),
                    data,
                )
        echo(
            f"Verification job created with name '{job.job_name}' and id -> {job.id} ✅"
        )
        with Live() as live:
            while True:
                current_job: Job = client.get(job.id, params={"kind": JobKind.VERIFY})
                if current_job.status == JobStatus.COMPLETED:
                    live.update(echo.format_message("Verification job is successful ✅"))
                    break
                elif current_job.status == JobStatus.FAILED:
                    live.update(
                        echo.format_error(
                            f"Verification Job with name '{current_job.job_name}' and id {current_job.id} failed"
                        )
                    )
                    sys.exit(1)
                else:
                    live.update(
                        echo.format_message(
                            f"Job status is '{current_job.status}', elapsed {current_job.elapsed_time}s"
                        )
                    )
                    time.sleep(20)
    except ValidationError as e:
        echo.error("Job validation error")
        echo.error("Review the provided information")
        if debug:
            raise e
        echo.error(str(e))
        sys.exit(1)
    except HTTPError as e:
        info = get_response_info(e.response)
        echo.error("⛔️Could not create the job")
        echo.error(f"⛔️Detail -> {info.get('detail')}⛔️")
        echo.error(f"⛔️Status code -> {info.get('status_code')}⛔️")
        echo.error(f"⛔️Error message -> {info.get('content')}⛔️")
        echo.error(
            f"⛔️Request ID: Give this to an administrator to trace the error -> {info.get('request_id')}⛔️"
        ) if info.get("request_id") else None
        if debug:
            raise e
        sys.exit(1)
