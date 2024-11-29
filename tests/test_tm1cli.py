import pytest
from typer.testing import CliRunner

from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("option", [None, ["--database", "mydb"], ["-d", "remotedb"]])
def test_tm1_version(option):
    if option:
        result = runner.invoke(app, ["tm1-version", *option])
    else:
        result = runner.invoke(app, ["tm1-version"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)


def test_whoami():
    result = runner.invoke(app, ["whoami"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert "Name" in result.stdout
    assert "FriendlyName" in result.stdout
    assert "Enabled" in result.stdout
    assert "Type" in result.stdout
    assert "Groups" in result.stdout


@pytest.mark.parametrize("option", [None, "--beautify", "-b"])
def test_threads(option):
    if option:
        result = runner.invoke(app, ["threads", option])
    else:
        result = runner.invoke(app, ["threads"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)


@pytest.mark.parametrize("command", ["list", "ls"])
def test_process_list(command):
    result = runner.invoke(app, ["process", command])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)


def test_process_exists():
    result = runner.invoke(app, ["process", "exists", "example"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "True\n" or result.stdout == "False\n"


def test_process_clone_missing_from_to():
    result = runner.invoke(app, ["process", "clone", "example"])
    assert result.exit_code == 1
    assert (
        "Error: Source database and target database must be different." in result.output
    )


def test_process_clone_not_exists():
    result = runner.invoke(app, ["process", "clone", "example", "--to", "remotedb"])
    assert result.exit_code == 1
    assert "Error: Process does not exist in source database!" in result.output


def test_process_clone_sucess(): ...


def test_process_dump_invalid_format(): ...


def test_process_dump_with_folder(): ...


def test_process_dump_process_not_exists(): ...


def test_process_dump_process_not_sucess(): ...
