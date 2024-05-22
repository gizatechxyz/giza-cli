from typing import Optional

import typer

from giza.cli.frameworks import cairo, ezkl
from giza.cli.options import (
    DEBUG_OPTION,
    FRAMEWORK_OPTION,
    MODEL_OPTION,
    VERSION_OPTION,
)
from giza.cli.utils.enums import Framework, JobSize

app = typer.Typer()


def verify(
    model_id: Optional[int] = MODEL_OPTION,
    version_id: Optional[int] = VERSION_OPTION,
    proof_id: Optional[int] = typer.Option(None, "--proof-id", "-p"),
    use_job: Optional[bool] = typer.Option(False, "--use-job"),
    proof: Optional[str] = typer.Option(None, "--proof", "-P"),
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    framework: Framework = FRAMEWORK_OPTION,
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if framework == Framework.CAIRO:
        cairo.verify(
            proof_id=proof_id,
            model_id=model_id,
            version_id=version_id,
            size=size,
            debug=debug,
            proof=proof,
            use_job=use_job,
        )
    elif framework == Framework.EZKL:
        ezkl.verify(
            proof_id=proof_id,
            model_id=model_id,
            version_id=version_id,
            size=size,
            debug=debug,
            proof=proof,
        )
    else:
        raise typer.BadParameter(
            f"Framework {framework} is not supported, please use one of the following: {Framework.CAIRO}, {Framework.EZKL}"
        )
