from typing import Annotated

import typer

from tm1cli.utils.cli_param import DATABASE_OPTION, INTERVAL_OPTION, WATCH_OPTION
from tm1cli.utils.generic import execute_exists, generic_list
from tm1cli.utils.watch import watch_option

app = typer.Typer()


@app.command(name="ls", help="Alias for list")
@app.command(name="list")
def list_dimension(
    ctx: typer.Context,
    database: Annotated[str, DATABASE_OPTION] = None,
    skip_control_dims: Annotated[
        bool,
        typer.Option(
            "-s",
            "--skip-control-cubes",
            help="Flag for not printing control cubes.",
        ),
    ] = False,
):
    """
    List dimensions
    """

    generic_list("dimensions", ctx, database, skip_control_dims=skip_control_dims)


@app.command()
@watch_option
def exists(
    ctx: typer.Context,
    dimension_name: str,
    database: Annotated[str, DATABASE_OPTION] = None,
    watch: Annotated[bool, WATCH_OPTION] = False,  # pylint: disable=unused-argument
    interval: Annotated[int, INTERVAL_OPTION] = 5,  # pylint: disable=unused-argument
):
    """
    Check if dimension exists
    """
    execute_exists(
        "dimensions",
        ctx,
        database,
        dimension_name=dimension_name,
    )
