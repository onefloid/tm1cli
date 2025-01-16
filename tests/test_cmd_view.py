import pytest
from typer.testing import CliRunner

from tm1cli.main import app

from .conftest import MockedTM1Service

runner = CliRunner()


@pytest.mark.parametrize(
    "options",
    [("not", "", "False"), ("example", "-p", "True"), ("not", "--private", "False")],
)
def test_view_exists(mocker, options):
    mocker.patch("tm1cli.commands.view.TM1Service", MockedTM1Service)
    if options[1]:
        result = runner.invoke(app, ["view", "exists", "example_cube", options[0]])
    else:
        result = runner.invoke(app, ["view", "exists", "example_cube", options[:1]])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == f"{options[2]}\n"


def test_view_list(mocker):
    mocker.patch("tm1cli.commands.view.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["view", "list", "example_cube"])

    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "View1\nView2\nView3\n"
