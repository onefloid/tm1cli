import typer
from rich import print
from TM1py.Services import TM1Service
from typing_extensions import Annotated

from tm1cli.utils import resolve_database

app = typer.Typer()

@app.command(name="ls", help="alias of list")
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

@app.command()
def clone(
    ctx: typer.Context,
    name: str,
    source_database: Annotated[
        str, typer.Option("--from", help="Specify the source database. Name from config needed.")
    ] =None,
    target_database: Annotated[
        str, typer.Option("--to", help="Specify the target database. Name from config needed.")
    ] =None,

):
    source_config = resolve_database(ctx, source_database)
    target_config = resolve_database(ctx, target_database)
    if source_config == target_config:
        print("[bold red]Error: Source database and target database must be different.[/bold red]")
        raise typer.Exit(code=1)
    
    with TM1Service(**source_config) as tm1:
        if not tm1.processes.exists(name):
            print("[bold red]Error: Process does not exist in source database![/bold red]")
            raise typer.Exit(code=1)
        process = tm1.processes.get(name)

    with TM1Service(**target_config) as tm1:
        response = tm1.processes.update_or_create(process)
        if response.ok:
            print(f"[bold green]Sucess: Process [italic]{name}[/italic] was cloned![/bold green]")
