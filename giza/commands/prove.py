import sys
import time
from typing import Optional

import typer
from pydantic import ValidationError
from requests import HTTPError
from rich.live import Live

from giza import API_HOST
from giza.client import JobsClient, ProofsClient
from giza.options import DEBUG_OPTION
from giza.schemas.jobs import Job, JobCreate
from giza.schemas.proofs import Proof
from giza.utils import echo, get_response_info
from giza.utils.enums import JobSize, JobStatus

app = typer.Typer()


def prove(
    program: str = typer.Argument(None),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    output_path: str = typer.Option("zk.proof", "--output-path", "-o"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    """
    Command to prove as spceific cairo program, previously converted to CASM.
    This will create a proving job and check the status, once it finishes if COMPLETED the proof is downloaded at the output path
    The daily jobs allowed are rate limited by the backend.

    Args:
        program: main CASM file
        size: Size of the job, allowed values are S, M, L and XL. Defaults to S.
        output_path: output path of the zk proof generated in the job
        debug (Optional[bool], optional): Whether to add debug information, will show requests, extra logs and traceback if there is an Exception. Defaults to DEBUG_OPTION (False).

    Raises:
        ValidationError: input fields are validated, if these are not suitable the exception is raised
        HTTPError: request error to the API, 4XX or 5XX
    """
    try:
        client = JobsClient(API_HOST)
        with open(program) as casm:
            job: Job = client.create(JobCreate(size=size), casm)
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
                    break
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
            echo(f"Proof Cairo VM execution time -> {proof.cairo_execution_time}s")
            echo(f"Proof proving time -> {proof.proving_time}s")
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
