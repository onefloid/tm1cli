from typing import Annotated

import typer
from rich import print
from TM1py.Services import TM1Service

from tm1cli.utils.cli_param import DATABASE_OPTION
from tm1cli.utils.various import resolve_database

app = typer.Typer()


@app.command(name="ls", help="Alias for list")
@app.command()
def list(
    ctx: typer.Context,
    database: Annotated[str, DATABASE_OPTION] = None,
    skip_control_cubes: Annotated[
        bool,
        typer.Option(
            "-s",
            "--skip-control-cubes",
            help="Flag for not printing control cubes.",
        ),
    ] = False,
):
    """
    List cubes
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        [print(cube) for cube in tm1.cubes.get_all_names(skip_control_cubes)]
