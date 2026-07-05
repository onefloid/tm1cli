# CLAUDE.md

Guidance for AI assistants (Claude Code) working in this repository.

## What this project is

**tm1cli** is a Python command-line interface for interacting with IBM Planning
Analytics / TM1 servers, built on top of [TM1py](https://github.com/cubewise-code/tm1py)
and [Typer](https://typer.tiangolo.com/). It's a small, published PyPI package
(`pip install tm1cli`), currently at version `0.1.7` (see `pyproject.toml`).

## Tech stack

- Python `^3.10`
- **Typer** — CLI framework (commands are plain functions decorated with `@app.command()`)
- **TM1py** — TM1 REST API client, used inside a `with TM1Service(...) as tm1:` context manager
- **Rich** — colored/table console output (`rich.print`, `rich.console.Console`, `rich.table.Table`)
- **PyYAML** — for `databases.yaml` config and process dump/load YAML serialization
- **Poetry** — dependency management and packaging (`poetry-core` build backend)
- Dev tools: **pytest** + **pytest-mock**, **pylint**, **isort**

## Repository layout

```
tm1cli/
  main.py                 # Typer app entrypoint; top-level commands (tm1-version, whoami, threads, version)
                           # and database config resolution (databases.yaml vs TM1_* env vars)
  commands/
    __init__.py            # re-exports all command submodules
    cube.py                 # `tm1cli cube ...`
    dimension.py             # `tm1cli dimension ...`
    process.py               # `tm1cli process ...` (list/exists/clone/dump/load)
    subset.py                 # `tm1cli subset ...`
    view.py                    # `tm1cli view ...`
  utils/
    cli_param.py            # shared typer.Option definitions (DATABASE_OPTION, WATCH_OPTION, INTERVAL_OPTION)
    various.py               # resolve_database(), print_error_and_exit()
    watch.py                  # @watch_option decorator for polling commands (--watch/-w, --interval)
    tm1yaml.py                # custom YAML dump/load for TM1py Process objects (multi-line script sections)
tests/
  conftest.py               # Mocked*Service classes + MockedTM1Service used to stub TM1py in tests
  test_tm1cli.py             # tests for top-level commands (tm1-version, whoami, threads, process ...)
  test_cmd_cubes.py           # cube command tests (uses mocker.patch to swap in MockedTM1Service)
  test_cmd_dimension.py
  test_cmd_subset.py
  test_cmd_view.py
databases.yaml.template     # example multi-database config; real databases.yaml is gitignored
pyproject.toml               # Poetry config, dependencies, `tm1cli` console script entry point
requirements.txt             # generated/plain pip requirements (kept in sync manually, used by pylint CI)
.pylintrc                    # pylint config
.github/workflows/
  pylint.yml                  # runs pylint on tm1cli/**/*.py for Python 3.10 and 3.11 on every push
  pypi-publish.yml             # builds and publishes to PyPI on GitHub release
CHANGELOG.md                  # manually maintained, one section per version
```

## Command architecture pattern

Each resource (cube, dimension, process, subset, view) has its own Typer
sub-app in `tm1cli/commands/<name>.py`, registered in `main.py` via:

```python
modules = [("process", commands.process), ("cube", commands.cube), ...]
for name, module in modules:
    app.add_typer(module.app, name=name)
```

A typical command function follows this shape:

```python
@app.command()
@watch_option
def exists(
    ctx: typer.Context,
    cube_name: str,
    database: Annotated[str, DATABASE_OPTION] = None,
    watch: Annotated[bool, WATCH_OPTION] = False,  # pylint: disable=unused-argument
    interval: Annotated[int, INTERVAL_OPTION] = 5,  # pylint: disable=unused-argument
):
    """Check if cube exists"""
    with TM1Service(**resolve_database(ctx, database)) as tm1:
        print(tm1.cubes.exists(cube_name))
```

Conventions to follow when adding or modifying commands:

- Always open the TM1py client as `with TM1Service(**resolve_database(ctx, database)) as tm1:` —
  never construct `TM1Service` outside a context manager.
- Every command accepts an optional `database: Annotated[str, DATABASE_OPTION] = None` parameter
  and resolves it via `resolve_database(ctx, database)`.
- `list` commands are also registered under the alias `ls` via a second
  `@app.command(name="ls", help="Alias for list")` decorator stacked above `@app.command(name="list")`.
  Follow this same double-decorator pattern for other aliases (e.g. `export`/`dump`, `import`/`load`
  in `process.py`).
- Commands that make sense to poll (existence checks) are decorated with `@watch_option` from
  `tm1cli/utils/watch.py` and take `watch`/`interval` parameters — mark them
  `# pylint: disable=unused-argument` since the decorator consumes them via `**kwargs`, not the
  function body.
- Use `rich.print` (imported `# pylint: disable=redefined-builtin`) for normal output, and
  `print_error_and_exit(msg)` from `tm1cli/utils/various.py` for user-facing errors — it prints in
  bold red and raises `typer.Exit(code=1)`. Don't raise raw exceptions for expected error paths.
- Reuse `DATABASE_OPTION`, `WATCH_OPTION`, `INTERVAL_OPTION` from `tm1cli/utils/cli_param.py` instead
  of redefining `typer.Option(...)` inline.

## Database configuration resolution

`main.py`'s `@app.callback()` builds `ctx.obj` once per invocation:

- If `databases.yaml` exists in the current working directory, it's parsed into
  `ctx.obj["configs"]` (keyed by database `name`) and `ctx.obj["default_db_config"]` (first entry).
- Otherwise, environment variables prefixed `TM1_` (e.g. `TM1_ADDRESS`, `TM1_PORT`, `TM1_SSL`,
  `TM1_USER`, `TM1_PASSWORD`) are lower-cased and stripped of the prefix to build
  `default_db_config`; `configs` is empty in this mode.
- `resolve_database(ctx, database_name)` in `tm1cli/utils/various.py` returns
  `default_db_config` when no `--database`/`-d` is given, otherwise looks up `database_name` in
  `configs` and calls `print_error_and_exit` if not found.
- The `--database`/`-d` option and `process clone --from/--to` **only work with a `databases.yaml`
  file** (env-var mode has no named configs) — preserve this constraint if touching this logic.

## Testing

- Test framework: `pytest` with `typer.testing.CliRunner` (`runner.invoke(app, [...])`) and
  `pytest-mock`'s `mocker` fixture.
- Two testing styles exist side by side:
  - `test_cmd_*.py` files mock TM1py entirely via `mocker.patch("tm1cli.commands.<module>.TM1Service", MockedTM1Service)`
    using the fake service classes in `tests/conftest.py` (`MockedCubeService`, `MockedViewService`,
    `MockedDimensionService`, `MockedSubsetService`, `MockedProcessService`, `MockedTM1Service`).
    These run without any real TM1 server and are the pattern to follow for new command tests.
  - `test_tm1cli.py` exercises top-level commands (`tm1-version`, `whoami`, `threads`, `process ...`)
    **without mocking TM1Service**, so it requires a real, reachable TM1 server configured via
    `databases.yaml` or `TM1_*` env vars (with a `mydb`/`remotedb` style config for the
    `--database`/`-d` parametrized cases). Don't assume these pass in a sandboxed environment with
    no TM1 server available.
- Several test functions in `test_tm1cli.py` are intentionally empty stubs (`def test_...(): ...`)
  — placeholders for not-yet-implemented coverage (e.g. `test_process_clone_sucess`,
  `test_process_dump_invalid_format`). Don't delete them without reason; filling them in is welcome.
- Run tests with `pytest` (mocked command tests only, if no TM1 server is available, target them
  explicitly, e.g. `pytest tests/test_cmd_cubes.py tests/test_cmd_dimension.py tests/test_cmd_subset.py tests/test_cmd_view.py`).
- There is no test job in CI today — `.github/workflows/pylint.yml` only runs pylint on `tm1cli/**/*.py`
  (Python 3.10 and 3.11); pytest is not invoked by GitHub Actions.

## Linting

- `pylint` is configured via `.pylintrc`: `max-line-length=120`, and
  `missing-module-docstring` / `missing-class-docstring` / `missing-function-docstring` /
  `too-many-arguments` / `too-many-positional-arguments` are disabled project-wide.
- Command docstrings are still used deliberately as Typer `--help` text (e.g. `"""List cubes"""`),
  so keep writing them even though pylint doesn't require them.
- CI runs `pylint $(git ls-files 'tm1cli/**/*.py')` — only the `tm1cli/` package is linted, not `tests/`.
- `isort` is a listed dev dependency for import ordering; keep imports grouped stdlib / third-party /
  local (`tm1cli...`), matching the existing files.

## Adding a new resource/command

1. Create `tm1cli/commands/<resource>.py` with its own `app = typer.Typer()`, following the pattern
   in an existing file (e.g. `cube.py` for a simple list/exists resource, `process.py` for a
   resource with more operations).
2. Add the import and `__all__` entry in `tm1cli/commands/__init__.py`.
3. Register it in the `modules` list in `tm1cli/main.py`.
4. Add mocked-service tests in `tests/test_cmd_<resource>.py` plus a corresponding
   `Mocked<Resource>Service` class in `tests/conftest.py`, mirroring the existing ones.
5. Add usage examples to the README's command list and a `CHANGELOG.md` entry under a new version
   heading (features / fixes / chore / docs sections, matching the existing style).

## Releasing

- Bump `version` in `pyproject.toml`.
- Add a new dated entry at the top of `CHANGELOG.md` (format: `## vX.Y.Z - YYYY-MM-DD` with
  `### Features` / `### Fix` / `### Chore` / `### Docs` / `### Breaking changes` subsections as needed).
- Publishing to PyPI happens via `.github/workflows/pypi-publish.yml`, triggered by creating a
  GitHub release (or manual `workflow_dispatch`) — it builds with `python -m build` and uses
  PyPI trusted publishing (no manual token needed).

## Things to watch out for

- `requirements.txt` is a separate, manually-tracked file from `poetry.lock`/`pyproject.toml` and is
  what the pylint CI workflow installs from — if you add/change a dependency in `pyproject.toml`,
  update `requirements.txt` too (or regenerate it) so CI installs the same set.
- `databases.yaml` is gitignored — never commit real credentials; use `databases.yaml.template` as
  the checked-in example and keep it in sync with any config schema changes.
- The custom YAML process (de)serialization in `tm1cli/utils/tm1yaml.py` renders TM1 process script
  sections (`PrologProcedure`, `MetadataProcedure`, `DataProcedure`, `EpilogProcedure`) as multi-line
  YAML block scalars specifically so process dumps are readable/diffable in git — preserve this
  behavior if touching `dump`/`load`.
