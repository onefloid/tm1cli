from typer.testing import CliRunner

from tm1cli.main import app

runner = CliRunner()

def test_tm1_version():
    result = runner.invoke(app, ["tm1-version"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)


