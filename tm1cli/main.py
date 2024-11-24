import json

import typer
import yaml
from rich import print
from rich.console import Console
from rich.table import Table
from TM1py import TM1Service
from typing_extensions import Annotated

import tm1cli.commands.process as process
from tm1cli.utils import resolve_database

console = Console()
app = typer.Typer()
app.add_typer(process.app, name="process")

@app.callback()
def main(ctx: typer.Context):
    """
    CLI tool to interact with TM1 using TM1py.
    """
    
    with open("databases.yaml", "r") as file:
        databases = yaml.safe_load(file)["databases"]
        configs = {db['name']: {key: value for key, value in db.items() if key != 'name'} for db in databases}
        default_db_config = databases[0]
        ctx.obj = {"configs": configs, "default_db_config": default_db_config}

@app.command()
def tm1_version(
    ctx: typer.Context,
    database: Annotated[
        str, typer.Option("--database", "-d", help="Specify the database to use")
    ] = None
):
    db_config = resolve_database(ctx, database)
    with TM1Service(**db_config) as tm1:
        version = tm1.server.get_product_version()
        print(version)

@app.command()
def threads(
    ctx: typer.Context,
    database: Annotated[
        str, typer.Option("--database", "-d", help="Specify the database to use")
    ] = None,
    beautify: Annotated[
        bool,
        typer.Option(
            "--beautify", "-b", help="Flag for printing a table."
        ),
    ] = False,
):
    db_config = resolve_database(ctx, database)
    with TM1Service(**db_config) as tm1:
        threads = tm1.sessions.get_threads_for_current()
        if beautify:
            table = Table(*threads[0].keys(), title="Threads")
            for thread in threads:
                table.add_row(*[str(value) for value in thread.values()])
            console.print(table)
        else:
            threads = json.dumps(threads, indent=4)
            print(threads)

if __name__ == "__main__":
    app()
