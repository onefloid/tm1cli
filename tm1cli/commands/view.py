from typing import Annotated

import typer
from rich import print  # pylint: disable=redefined-builtin
from TM1py.Services import TM1Service

from tm1cli.utils.cli_param import DATABASE_OPTION
from tm1cli.utils.various import resolve_database

app = typer.Typer()


@app.command(name="ls", help="Alias for list")
@app.command(name="list")
def list_view(
    ctx: typer.Context,
    cube_name: str,
    database: Annotated[str, DATABASE_OPTION] = None,
):
    """
    List views
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        for view in tm1.views.get_all_names(cube_name):
            print(view)
