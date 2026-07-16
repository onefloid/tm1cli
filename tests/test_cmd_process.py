import pytest
from typer.testing import CliRunner

from tests.conftest import MockedTM1Service
from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("command", ["list", "ls"])
@pytest.mark.parametrize(
    "raw_option,expected_output",
    [
        (None, "- Process1\n- Process2\n"),
        ("--output-raw", "Process1\nProcess2\n"),
    ],
)
def test_process_list(mocker, command, raw_option, expected_output):
    mocker.patch("tm1cli.utils.generic.TM1Service", MockedTM1Service)
    args = [raw_option] if raw_option else []
    args += ["process", command]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == expected_output


@pytest.mark.parametrize(
    "raw_option,expected_output",
    [(None, "✅ Process exists!\n"), ("--output-raw", "True\n")],
)
def test_process_exists(mocker, raw_option, expected_output):
    mocker.patch("tm1cli.utils.generic.TM1Service", MockedTM1Service)
    if raw_option:
        result = runner.invoke(app, [raw_option, "process", "exists", "example"])
    else:
        result = runner.invoke(app, ["process", "exists", "example"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == expected_output
