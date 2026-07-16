from typing import Annotated

import typer

from tm1cli.utils.cli_param import DATABASE_OPTION, INTERVAL_OPTION, WATCH_OPTION
from tm1cli.utils.generic import execute_exists, generic_list
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

    generic_list("views", ctx, database, cube_name=cube_name)


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

    execute_exists(
        "views",
        ctx,
        database,
        cube_name=cube_name,
        view_name=view_name,
        private=is_private,
    )
