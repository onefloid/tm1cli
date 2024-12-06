import pytest
from typer.testing import CliRunner

from tests.conftest import MockedTM1Service
from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("command", ["list", "ls"])
def test_cube_list(mocker, command):
    mocker.patch("tm1cli.commands.cube.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["cube", command])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "Cube1\nCube2\n"


def test_cube_exists(mocker):
    mocker.patch("tm1cli.commands.cube.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["cube", "exists", "Cube1"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "True\n"
