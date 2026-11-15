import pandas as pd
import pytest

from practice import load

m = load(__file__)


@pytest.fixture
def raw():
    return pd.read_csv(m.DATA)


def test_missing_report(raw):
    report = m.missing_report(raw)
    assert report == {"station": 1, "temp_c": 2, "humidity": 1}
    assert all(type(v) is int for v in report.values())


def test_missing_report_nothing_missing():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    assert m.missing_report(df) == {}


def test_clean_shape_and_no_missing(raw):
    result = m.clean(raw)
    assert len(result) == 6
    assert result.isna().sum().sum() == 0
    assert result.index.tolist() == [0, 1, 2, 3, 4, 5]


def test_clean_fills_temperature_with_station_mean(raw):
    result = m.clean(raw)
    assert result["temp_c"].tolist() == [4.0, 5.0, 6.0, 12.0, 14.0, 13.0]


def test_clean_fills_humidity_with_median(raw):
    result = m.clean(raw)
    assert result["humidity"].tolist() == [80.0, 78.0, 64.0, 60.0, 62.0, 64.0]


def test_clean_keeps_row_order_and_columns(raw):
    result = m.clean(raw)
    assert result.columns.tolist() == ["station", "date", "temp_c", "humidity"]
    assert result["date"].tolist()[:3] == ["2024-03-01", "2024-03-02", "2024-03-03"]
    assert "" not in result["station"].tolist()


def test_clean_does_not_change_input(raw):
    before = raw.copy()
    assert m.clean(raw) is not None
    pd.testing.assert_frame_equal(raw, before)
