from typing import Annotated

import typer
from rich import print  # pylint: disable=redefined-builtin
from TM1py.Services import TM1Service

from tm1cli.utils.cli_param import DATABASE_OPTION
from tm1cli.utils.various import resolve_database

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

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        for dim in tm1.dimensions.get_all_names(skip_control_dims):
            print(dim)


@app.command()
def exists(
    ctx: typer.Context,
    dimension_name: str,
    database: Annotated[str, DATABASE_OPTION] = None,
):
    """
    Check if dimension exists
    """
    with TM1Service(**resolve_database(ctx, database)) as tm1:
        print(tm1.dimensions.exists(dimension_name))
