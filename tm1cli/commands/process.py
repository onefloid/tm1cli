import json
from pathlib import Path

import typer
from rich import print
from TM1py.Objects import Process
from TM1py.Services import TM1Service
from typing_extensions import Annotated

from tm1cli.utils import print_error_and_exit, resolve_database
from tm1cli.Utils.cli_param import DATABASE_OPTION
from tm1cli.Utils.tm1yaml import dump_process, load_process

app = typer.Typer()

def _get_process(name: str, database_config: dict) -> Process:
    with TM1Service(**database_config) as tm1:
        if not tm1.processes.exists(name):
            print_error_and_exit("Process does not exist in source database!")
        process = tm1.processes.get(name)
    return process


@app.command(name="ls", help="alias of list")
@app.command()
def list(
    ctx: typer.Context,
    database: Annotated[str, DATABASE_OPTION] = None,
):
    """
    Shows a process list
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        [print(process) for process in tm1.processes.get_all_names()]


@app.command()
def exists(
    ctx: typer.Context,
    name: str,
    database: Annotated[str, DATABASE_OPTION] = None,
):
    """
    Shows if process exists
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
    """
    Clones a process from one database to another database
    """
    source_config = resolve_database(ctx, source_database)
    target_config = resolve_database(ctx, target_database)
    if source_config == target_config:
        print_error_and_exit("Source database and target database must be different.")
    
    process = _get_process(name, source_config)

    with TM1Service(**target_config) as tm1:
        response = tm1.processes.update_or_create(process)
        if response.ok:
            print(f"[bold green]Sucess: Process [italic]{name}[/italic] was cloned![/bold green]")

@app.command()
def dump(
    ctx: typer.Context,
    name: str,
    output_folder: Annotated[str, typer.Option("--folder", help="Specify the file where the process is dumped to")] = ".",
    format: Annotated[str, typer.Option("--format", help="Specify the output format of ")] = "yaml",
    database: Annotated[str, DATABASE_OPTION] = None,
):
    """
    Dumps a process from a TM1 database to a file
    """

    database_config = resolve_database(ctx, database)
    process = _get_process(name, database_config)

    if format == "json": 
        with open(Path(output_folder, f"{name}.json"), "w") as json_file:
            json.dump(json.loads(process.body), json_file, indent=4)
    elif format == "yaml":
        with open(Path(output_folder, f"{name}.yaml"), "w", encoding="utf-8") as yaml_file:
            yaml_file.write(dump_process(process))
    else:
        print_error_and_exit(f"The format: {format} is not valid. Valid formats are json or yaml.")

@app.command()
def load(
    ctx: typer.Context,
    name: str,
    input_folder: Annotated[str, typer.Option("--folder", help="Specify the folder from where the file is loaded")] = ".",
    format: Annotated[str, typer.Option("--format", help="Specify the input format")] = "yaml",
    database: Annotated[str, DATABASE_OPTION] = None,
):
    """
    Loads a process from a file into a TM1 database
    """

    database_config = resolve_database(ctx, database)

    if format == "json": 
        with open(Path(input_folder, f"{name}.json"), "r") as json_file:
            process = Process.from_json(json_file.read())
    elif format == "yaml":
        with open(Path(input_folder, f"{name}.yaml"), "r", encoding="utf-8") as yaml_file:
            process = load_process(yaml_file.read())
    else:
        print(f"[bold red]Error: The format: {format} is not valid. Valid formats are json or yaml.[/bold red]")
        raise typer.Exit(code=1)
    
    with TM1Service(**database_config) as tm1:
        response = tm1.processes.update_or_create(process)
        if response.ok:
            print(f"[bold green]Sucess: Process [italic]{name}[/italic] was loaded in TM1 Database![/bold green]")
