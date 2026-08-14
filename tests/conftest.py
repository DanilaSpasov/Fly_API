import pytest

from src.models import Aeroplane


@pytest.fixture()
def aeroplane():
    """Возвращает тестовый экземпляр самолёта."""
    return Aeroplane(
        "abc123",
        "TEST123",
        "Canada",
        1000.0,
        False,
        200.0,
    )


@pytest.fixture()
def aeroplanes(aeroplane):
    """Возвращает список тестовых самолётов."""
    return [
        aeroplane,
        Aeroplane(
            "def456",
            "HIGH456",
            "Germany",
            3000.0,
            False,
            250.0,
        ),
        Aeroplane(
            "ghi789",
            "MIDDLE789",
            "United States",
            2000.0,
            True,
            150.0,
        ),
    ]


@pytest.fixture()
def state():
    """Возвращает тестовое состояние самолёта в формате API."""
    return [
        "abc123",
        " TEST123 ",
        "Canada",
        None,
        None,
        None,
        None,
        1000.0,
        False,
        200.0,
    ]
