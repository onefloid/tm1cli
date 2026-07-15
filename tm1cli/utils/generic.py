import typer
from rich import print  # pylint: disable=redefined-builtin
from TM1py import TM1Service

from tm1cli.utils.various import resolve_database

SINGULAR_NAMES = {
    "cubes": "Cube",
    "dimensions": "Dimension",
    "processes": "Process",
    "subsets": "Subset",
    "views": "View",
}


def execute_exists(attribute_name, ctx, database, **args):
    """
    Util function to execute an exists function
    """

    database_config = resolve_database(ctx, database)

    try:
        with TM1Service(**database_config) as tm1:
            attribute = getattr(tm1, attribute_name)
            output = attribute.exists(**args)
    except (AttributeError, TypeError):
        # Programming errors (wrong attribute_name or mismatched kwargs),
        # not TM1 runtime errors - let them raise as real tracebacks.
        raise
    except Exception as e:  # pylint: disable=broad-except
        print(f"[bold red]{type(e).__name__}:[/bold red] {e}")
        raise typer.Exit(code=1) from e

    if ctx.obj["raw"]:
        print(output)
        return

    output_name = SINGULAR_NAMES[attribute_name]
    if output:
        print(f":white_check_mark: {output_name} exists!")
    else:
        print(f":x: {output_name} does not exist!")
