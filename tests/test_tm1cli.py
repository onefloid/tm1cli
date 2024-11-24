import pytest
from typer.testing import CliRunner

from tm1cli.main import app

runner = CliRunner()

def test_tm1_version():
    result = runner.invoke(app, ["tm1-version"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)

@pytest.mark.parametrize("option", [None, "--beautify", "-b"])
def test_threads(option):
    if (option):
        result = runner.invoke(app, ["threads", option])
    else:
        result = runner.invoke(app, ["threads"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)