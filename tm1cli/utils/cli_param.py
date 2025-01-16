import typer

DATABASE_OPTION = typer.Option("--database", "-d", help="Specify the database to use")
WATCH_OPTION = typer.Option(
    "--watch", "-w", help="Watch the command output periodically."
)
INTERVAL_OPTION = (
    typer.Option("--interval", help="Interval in seconds for the watch option."),
)
