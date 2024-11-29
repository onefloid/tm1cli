import typer
from rich import print as rich_print


def resolve_database(ctx: typer.Context, database_name: str) -> dict:
    """
    Resolves the database name to its configuration.
    If no database is specified, use the default database.
    """
    if not database_name:
        return ctx.obj.get("default_db_config")
    configs = ctx.obj.get("configs")
    if database_name not in configs:
        print_error_and_exit(
            f"Database '{database_name}' not found in configuration file: databases.yaml."
        )
    return configs[database_name]


def print_error_and_exit(msg: str) -> None:
    """
    Prints an error to STDOUT and exits the script with error code 1.
    """
    rich_print(f"[bold red]Error: {msg} [/bold red]")
    raise typer.Exit(code=1)
