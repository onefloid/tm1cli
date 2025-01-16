from typing import Annotated

import typer
from rich import print  # pylint: disable=redefined-builtin
from TM1py.Services import TM1Service

from tm1cli.utils.cli_param import DATABASE_OPTION, INTERVAL_OPTION, WATCH_OPTION
from tm1cli.utils.various import resolve_database
from tm1cli.utils.watch import watch_option

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


@app.command()
@watch_option
def exists(
    ctx: typer.Context,
    cube_name: str,
    view_name: str,
    is_private: Annotated[
        bool, typer.Option("-p", "--private", help="Flag to specify if view is private")
    ] = False,
    database: Annotated[str, DATABASE_OPTION] = None,
    watch: Annotated[bool, WATCH_OPTION] = False,  # pylint: disable=unused-argument
    interval: Annotated[int, INTERVAL_OPTION] = 5,  # pylint: disable=unused-argument
):
    """
    Check if view exists
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        print(tm1.views.exists(cube_name, view_name, is_private))
