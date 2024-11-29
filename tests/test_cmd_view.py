import pytest
from typer.testing import CliRunner

from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("command", ["list", "ls"])
def test_cube_list(command):
    result = runner.invoke(
        app,
        [
            "view",
            command,
            "TM1py_tests_annotations_0f680909_74b1_11ef_b4ba_546ceb97bbfb",
        ],
    )
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
