import pytest
from typer.testing import CliRunner

from tm1cli.main import app

runner = CliRunner()

@pytest.mark.parametrize("command", ["list", "ls"])
def test_cube_list(command):
    result = runner.invoke(app, ["cube", command])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)