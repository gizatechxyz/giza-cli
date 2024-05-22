from typing import List, Optional

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


def prove(
    data: List[str] = typer.Argument(None),
    model_id: Optional[int] = MODEL_OPTION,
    version_id: Optional[int] = VERSION_OPTION,
    size: JobSize = typer.Option(JobSize.S, "--size", "-s"),
    framework: Framework = FRAMEWORK_OPTION,
    output_path: str = typer.Option("zk.proof", "--output-path", "-o"),
    debug: Optional[bool] = DEBUG_OPTION,
) -> None:
    if framework == Framework.CAIRO:
        cairo.prove(data=data, size=size, output_path=output_path, debug=debug)
    elif framework == Framework.EZKL:
        ezkl.prove(
            input_data=data[0],
            model_id=model_id,
            version_id=version_id,
            size=size,
            output_path=output_path,
            debug=debug,
        )
    else:
        raise typer.BadParameter(
            f"Framework {framework} is not supported, please use one of the following: {Framework.CAIRO}, {Framework.EZKL}"
        )
