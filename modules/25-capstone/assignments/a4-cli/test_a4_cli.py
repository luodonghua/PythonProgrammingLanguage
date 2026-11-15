import pytest

from practice import load

m = load(__file__)


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "test.db")


def run(db, *args):
    return m.main(["--db", db, *args])


def test_add_prints_confirmation_and_returns_zero(db, capsys):
    assert run(db, "add", "2024-03-01", "Food", "45.5", "-d", "Groceries") == 0
    out = capsys.readouterr().out
    assert out == "Added #1: 2024-03-01 food 45.50\n"


def test_ids_increase(db, capsys):
    run(db, "add", "2024-03-01", "food", "1")
    run(db, "add", "2024-03-02", "food", "2")
    assert capsys.readouterr().out.splitlines()[-1].startswith("Added #2:")


def test_list_shows_expenses_in_date_order(db, capsys):
    run(db, "add", "2024-03-05", "food", "12.25", "--description", "Lunch")
    run(db, "add", "2024-03-01", "transport", "30", "-d", "Bus pass")
    capsys.readouterr()
    assert run(db, "list") == 0
    assert capsys.readouterr().out.splitlines() == [
        "2024-03-01  transport       30.00  Bus pass",
        "2024-03-05  food            12.25  Lunch",
    ]


def test_list_line_without_description_has_no_trailing_spaces(db, capsys):
    run(db, "add", "2024-03-01", "food", "3")
    capsys.readouterr()
    run(db, "list")
    assert capsys.readouterr().out == "2024-03-01  food             3.00\n"


def test_list_empty(db, capsys):
    assert run(db, "list") == 0
    assert capsys.readouterr().out == "No expenses.\n"


def test_list_with_month_filter(db, capsys):
    run(db, "add", "2024-03-01", "food", "1")
    run(db, "add", "2024-04-01", "food", "2")
    capsys.readouterr()
    assert run(db, "list", "--month", "2024-04") == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == ["2024-04-01  food             2.00"]


def test_report_prints_table(db, capsys):
    run(db, "add", "2024-03-01", "food", "45.50")
    run(db, "add", "2024-03-05", "food", "12.25")
    run(db, "add", "2024-03-03", "transport", "30")
    capsys.readouterr()
    assert run(db, "report", "2024-03") == 0
    out = capsys.readouterr().out
    assert out.splitlines()[0] == "Expenses for 2024-03"
    assert "food             2       57.75" in out
    assert out.splitlines()[-1] == "TOTAL            3       87.75"


def test_report_empty_month(db, capsys):
    assert run(db, "report", "2024-03") == 0
    assert capsys.readouterr().out == "No expenses for 2024-03\n"


@pytest.mark.parametrize(
    "args",
    [
        ("add", "2024-02-30", "food", "5"),
        ("add", "yesterday", "food", "5"),
        ("add", "2024-03-01", "food", "abc"),
        ("add", "2024-03-01", "food", "-5"),
        ("add", "2024-03-01", "food", "0"),
        ("add", "2024-03-01", "food", "1.999"),
        ("add", "2024-03-01", "food", "NaN"),
        ("add", "2024-03-01", "   ", "5"),
        ("report", "2024-13"),
        ("report", "March"),
        ("list", "--month", "24-03"),
    ],
)
def test_invalid_input_returns_one_and_writes_to_stderr(db, capsys, args):
    assert run(db, *args) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("error: ")


def test_invalid_add_stores_nothing(db, capsys):
    run(db, "add", "2024-03-01", "food", "abc")
    capsys.readouterr()
    run(db, "list")
    assert capsys.readouterr().out == "No expenses.\n"


@pytest.mark.parametrize("args", [(), ("frobnicate",), ("add", "2024-03-01"), ("report",)])
def test_usage_errors_exit_with_two(db, capsys, args):
    with pytest.raises(SystemExit) as info:
        run(db, *args)
    assert info.value.code == 2


def test_help_exits_zero(capsys):
    with pytest.raises(SystemExit) as info:
        m.main(["--help"])
    assert info.value.code == 0
    assert "add" in capsys.readouterr().out


def test_parse_amount():
    from decimal import Decimal

    assert m.parse_amount("12.5") == Decimal("12.5")
    assert m.parse_amount(" 7 ") == Decimal("7")
    for bad in ("x", "", "0", "-1", "1.001", "Infinity"):
        with pytest.raises(ValueError):
            m.parse_amount(bad)


def test_build_parser_defaults():
    args = m.build_parser().parse_args(["list"])
    assert args.db == "expenses.db"
    assert args.command == "list"
    assert args.month is None
