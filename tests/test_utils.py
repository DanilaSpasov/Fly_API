import pytest

from src.utils import (
    filter_aeroplanes_by_countries,
    get_top_aeroplanes_by_altitude,
    parse_countries,
)


def test_parse_countries():
    """Проверяет разбор строки со списком стран."""
    result = parse_countries(" Canada, United States, , Germany ")

    assert result == ["Canada", "United States", "Germany"]


def test_parse_empty_countries():
    """Проверяет разбор пустой строки со странами."""
    assert parse_countries("   ") == []


def test_filter_aeroplanes_by_countries(aeroplanes):
    """Проверяет фильтрацию самолётов по странам."""
    result = filter_aeroplanes_by_countries(
        aeroplanes,
        ["canada", "GERMANY"],
    )

    assert [aeroplane.icao24 for aeroplane in result] == ["abc123", "def456"]


def test_filter_without_countries_returns_copy(aeroplanes):
    """Проверяет возврат копии списка без фильтра стран."""
    result = filter_aeroplanes_by_countries(aeroplanes, [])

    assert result == aeroplanes
    assert result is not aeroplanes


def test_get_top_aeroplanes_by_altitude(aeroplanes):
    """Проверяет выбор самых высоко летящих самолётов."""
    result = get_top_aeroplanes_by_altitude(aeroplanes, 2)

    assert [aeroplane.icao24 for aeroplane in result] == ["def456", "ghi789"]


@pytest.mark.parametrize("top_n", [True, 2.5, "2"])
def test_get_top_with_wrong_type(aeroplanes, top_n):
    """Проверяет отклонение неверного типа размера выборки."""
    with pytest.raises(TypeError):
        get_top_aeroplanes_by_altitude(aeroplanes, top_n)


@pytest.mark.parametrize("top_n", [0, -1])
def test_get_top_with_wrong_value(aeroplanes, top_n):
    """Проверяет отклонение неверного значения размера выборки."""
    with pytest.raises(ValueError):
        get_top_aeroplanes_by_altitude(aeroplanes, top_n)
