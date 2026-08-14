import pytest

from src.models import Aeroplane


def test_aeroplane_init(aeroplane):
    """Проверяет инициализацию всех полей самолёта."""
    assert aeroplane.icao24 == "abc123"
    assert aeroplane.callsign == "TEST123"
    assert aeroplane.origin_country == "Canada"
    assert aeroplane.altitude == 1000.0
    assert aeroplane.on_ground is False
    assert aeroplane.velocity == 200.0


@pytest.mark.parametrize("altitude", [True, "1000", None])
def test_invalid_altitude(altitude):
    """Проверяет отклонение некорректного типа высоты."""
    with pytest.raises(TypeError):
        Aeroplane("abc123", "TEST123", "Canada", altitude, False, 200.0)


@pytest.mark.parametrize("velocity", [False, "200", None])
def test_invalid_velocity(velocity):
    """Проверяет отклонение некорректного типа скорости."""
    with pytest.raises(TypeError):
        Aeroplane("abc123", "TEST123", "Canada", 1000.0, False, velocity)


def test_negative_velocity():
    """Проверяет отклонение отрицательной скорости."""
    with pytest.raises(ValueError):
        Aeroplane("abc123", "TEST123", "Canada", 1000.0, False, -1.0)


def test_is_faster_than(aeroplanes):
    """Проверяет сравнение самолётов по скорости."""
    assert aeroplanes[1].is_faster_than(aeroplanes[0]) is True
    assert aeroplanes[2].is_faster_than(aeroplanes[0]) is False


def test_is_faster_than_wrong_type(aeroplane):
    """Проверяет ошибку сравнения скорости с объектом другого типа."""
    with pytest.raises(TypeError):
        aeroplane.is_faster_than("not an aeroplane")


def test_is_higher_than(aeroplanes):
    """Проверяет сравнение самолётов по высоте."""
    assert aeroplanes[1].is_higher_than(aeroplanes[0]) is True
    assert aeroplanes[0].is_higher_than(aeroplanes[2]) is False


def test_is_higher_than_wrong_type(aeroplane):
    """Проверяет ошибку сравнения высоты с объектом другого типа."""
    with pytest.raises(TypeError):
        aeroplane.is_higher_than("not an aeroplane")


def test_from_state(state):
    """Проверяет создание самолёта из состояния API."""
    aeroplane = Aeroplane.from_state(state)

    assert aeroplane.icao24 == "abc123"
    assert aeroplane.callsign == "TEST123"
    assert aeroplane.origin_country == "Canada"
    assert aeroplane.altitude == 1000.0
    assert aeroplane.on_ground is False
    assert aeroplane.velocity == 200.0


def test_from_state_without_callsign(state):
    """Проверяет подстановку позывного при его отсутствии."""
    state[1] = None

    aeroplane = Aeroplane.from_state(state)

    assert aeroplane.callsign == "Неизвестно"


def test_cast_to_object_list(state):
    """Проверяет фильтрацию некорректных состояний при создании самолётов."""
    short_state = ["short"]
    state_without_altitude = state.copy()
    state_without_altitude[7] = None
    state_without_velocity = state.copy()
    state_without_velocity[9] = None

    result = Aeroplane.cast_to_object_list(
        [state, short_state, state_without_altitude, state_without_velocity]
    )

    assert len(result) == 1
    assert result[0].icao24 == "abc123"


def test_aeroplane_str(aeroplane):
    """Проверяет строковое представление самолёта."""
    assert str(aeroplane) == (
        "Позывной: TEST123, страна регистрации: Canada, "
        "скорость: 200.0 м/с, высота: 1000.0 м."
    )
