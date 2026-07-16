import pytest
from typer.testing import CliRunner

from tm1cli.main import app

from .conftest import MockedTM1Service

runner = CliRunner()


@pytest.mark.parametrize(
    "view_name,private_flag,exists_result",
    [("not", "", False), ("example", "-p", True), ("not", "--private", False)],
)
@pytest.mark.parametrize("raw_option", [None, "--output-raw"])
def test_view_exists(mocker, view_name, private_flag, exists_result, raw_option):
    mocker.patch("tm1cli.utils.generic.TM1Service", MockedTM1Service)
    args = [raw_option] if raw_option else []
    args += ["view", "exists", "example_cube", view_name]
    if private_flag:
        args.append(private_flag)
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    if raw_option:
        assert result.stdout == f"{exists_result}\n"
    else:
        icon = "✅" if exists_result else "❌"
        word = "exists" if exists_result else "does not exist"
        assert result.stdout == f"{icon} View {word}!\n"


@pytest.mark.parametrize(
    "raw_option,expected_output",
    [
        (None, "- View1\n- View2\n- View3\n"),
        ("--output-raw", "View1\nView2\nView3\n"),
    ],
)
def test_view_list(mocker, raw_option, expected_output):
    mocker.patch("tm1cli.utils.generic.TM1Service", MockedTM1Service)
    args = [raw_option] if raw_option else []
    args += ["view", "list", "example_cube"]
    result = runner.invoke(app, args)

    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == expected_output
