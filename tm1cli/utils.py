import typer
from rich import print


def resolve_database(ctx: typer.Context, database_name: str) -> dict:
    """
    Resolves the database name to its configuration.
    If no database is specified, use the default database.
    """
    if not database_name:
        return ctx.obj.get("default_db_config")
    configs = ctx.obj.get("configs")
    if database_name not in configs:
        print(
            f"[bold red]Error: Database '{database_name}' not found in configuration file: databases.yaml.[/bold red]"
        )
        raise typer.Exit(code=1)
    return configs[database_name]