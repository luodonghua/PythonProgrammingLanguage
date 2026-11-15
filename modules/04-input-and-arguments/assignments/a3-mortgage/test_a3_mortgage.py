import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("principal", "rate", "years", "expected"),
    [
        (200_000, 6, 30, 1199.10),
        (120_000, 0, 10, 1000.00),
        (150_000, 4.5, 15, 1147.49),
        (1_000, 12, 1, 88.85),
    ],
)
def test_monthly_payment(principal, rate, years, expected):
    assert m.monthly_payment(principal, rate, years) == pytest.approx(expected, abs=0.005)


def test_monthly_payment_is_rounded():
    value = m.monthly_payment(200_000, 6, 30)
    assert value == round(value, 2)


@pytest.mark.parametrize(
    ("principal", "rate", "years"),
    [(0, 5, 10), (-100, 5, 10), (1000, -1, 10), (1000, 5, 0)],
)
def test_monthly_payment_invalid(principal, rate, years):
    with pytest.raises(ValueError):
        m.monthly_payment(principal, rate, years)


def test_main_success(capsys):
    assert m.main(["200000", "6", "30"]) == 0
    captured = capsys.readouterr()
    assert captured.out.splitlines() == ["Monthly payment: 1,199.10", "Total paid: 431,676.00"]
    assert captured.err == ""


def test_main_zero_rate(capsys):
    assert m.main(["1200", "0", "1"]) == 0
    assert capsys.readouterr().out.splitlines() == ["Monthly payment: 100.00", "Total paid: 1,200.00"]


@pytest.mark.parametrize("argv", [["0", "6", "30"], ["1000", "-1", "3"], ["1000", "5", "0"]])
def test_main_invalid_values(capsys, argv):
    assert m.main(argv) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("error: ")


@pytest.mark.parametrize("argv", [[], ["1000", "5"], ["abc", "5", "3"], ["1000", "5", "2.5"]])
def test_main_usage_errors(capsys, argv):
    with pytest.raises(SystemExit) as info:
        m.main(argv)
    assert info.value.code == 2
