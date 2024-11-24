import json

import typer
import yaml
from TM1py import TM1Service
from typing_extensions import Annotated

app = typer.Typer()

# Global state to store loaded configurations
configs = {}
default_db_config = {}

def resolve_database(database_name: str) -> dict:
    """
    Resolves the database name to its configuration.
    If no database is specified, use the default database.
    """
    if not database_name:
        return default_db_config
    
    if database_name not in configs:
        typer.echo(f"Error: Database '{database_name}' not found in configuration file: databases.yaml.")
        raise typer.Exit(code=1)
    
    return configs[database_name]

@app.callback()
def main():
    """
    CLI tool to interact with TM1 using TM1py.
    """
    
    with open("databases.yaml", "r") as file:
        global configs, default_db_config
        databases = yaml.safe_load(file)["databases"]
        configs = {db['name']: {key: value for key, value in db.items() if key != 'name'} for db in databases}
        default_db_config = databases[0]

@app.command()
def tm1_version(
    database: Annotated[
        str, typer.Option("--database", "-d", help="Specify the database to use")
    ] = None
):
    with TM1Service(**default_db_config) as tm1:
        version = tm1.server.get_product_version()
        print(version)

@app.command()
def threads(
    database: Annotated[
        str, typer.Option("--database", "-d", help="Specify the database to use")
    ] = None,
    beautify: Annotated[
        bool,
        typer.Option(
            "--beautify", "-b", help="Flag for printing json return with indentation."
        ),
    ] = False,
):
    db_config = resolve_database(database)
    with TM1Service(**db_config) as tm1:
        threads = tm1.sessions.get_threads_for_current()
        if beautify:
            threads = json.dumps(threads, indent=4)
        print(threads)


if __name__ == "__main__":
    app()
