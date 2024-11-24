import typer
from TM1py.Services import TM1Service
from typing_extensions import Annotated

from tm1cli.utils import resolve_database

# from TM1py.Objects import Process

app = typer.Typer()


@app.command()
def list(
    ctx: typer.Context,
    database: Annotated[
        str, typer.Option("--database", "-d", help="Specify the database to use")
    ] = None,
):
    """
    Show if process exists
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        [print(process) for process in tm1.processes.get_all_names()]


@app.command()
def exists(
    ctx: typer.Context,
    name: str,
    database: Annotated[
        str, typer.Option("--database", "-d", help="Specify the database to use")
    ] = None,
):
    """
    Show if process exists
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        print(tm1.processes.exists(name))
