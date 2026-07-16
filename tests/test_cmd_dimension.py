import pytest
from typer.testing import CliRunner

from tests.conftest import MockedTM1Service
from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("command", ["list", "ls"])
@pytest.mark.parametrize(
    "raw_option,expected_output",
    [
        (None, "- Dimension1\n- Dimension2\n- Dimension3\n"),
        ("--output-raw", "Dimension1\nDimension2\nDimension3\n"),
    ],
)
def test_dimension_list(mocker, command, raw_option, expected_output):
    mocker.patch("tm1cli.utils.generic.TM1Service", MockedTM1Service)
    args = [raw_option] if raw_option else []
    args += ["dimension", command]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == expected_output


@pytest.mark.parametrize(
    "raw_option,expected_output",
    [(None, "✅ Dimension exists!\n"), ("--output-raw", "True\n")],
)
def test_dimension_exists(mocker, raw_option, expected_output):
    mocker.patch("tm1cli.utils.generic.TM1Service", MockedTM1Service)
    if raw_option:
        result = runner.invoke(app, [raw_option, "dimension", "exists", "Dimension1"])
    else:
        result = runner.invoke(app, ["dimension", "exists", "Dimension1"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == expected_output
