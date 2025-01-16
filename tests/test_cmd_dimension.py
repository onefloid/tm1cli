import pytest
from typer.testing import CliRunner

from tests.conftest import MockedTM1Service
from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("command", ["list", "ls"])
def test_dimension_list(mocker, command):
    mocker.patch("tm1cli.commands.dimension.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["dimension", command])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "Dimension1\nDimension2\nDimension3\n"


def test_dimension_exists(mocker):
    mocker.patch("tm1cli.commands.dimension.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["dimension", "exists", "Dimension1"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "True\n"
