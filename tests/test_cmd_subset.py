import pytest
from typer.testing import CliRunner

from tests.conftest import MockedTM1Service
from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("command", ["list", "ls"])
def test_subset_list(mocker, command):
    mocker.patch("tm1cli.commands.subset.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["subset", command, "Dimension1"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "Subset1\nSubset2\nSubset3\n"


@pytest.mark.parametrize(
    "raw_option,expected_output",
    [(None, "✅ Subset exists!\n"), ("--output-raw", "True\n")],
)
def test_subset_exists(mocker, raw_option, expected_output):
    mocker.patch("tm1cli.utils.generic.TM1Service", MockedTM1Service)
    if raw_option:
        result = runner.invoke(
            app, [raw_option, "subset", "exists", "Dimension1", "Subset1"]
        )
    else:
        result = runner.invoke(app, ["subset", "exists", "Dimension1", "Subset1"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == expected_output
