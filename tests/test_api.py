from unittest.mock import Mock
from unittest.mock import patch

import pytest
from requests import RequestException

from src.api import AbstractAPI
from src.api import AeroplanesAPI


def test_abstract_api():
    """Проверяет, что абстрактный API нельзя создать напрямую."""
    with pytest.raises(TypeError):
        AbstractAPI()


@patch("src.api.requests.get")
def test_get_country_bounds(mock_get):
    """Проверяет получение границ страны из ответа API."""
    mock_response = Mock()
    mock_response.json.return_value = [
        {"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}
    ]
    mock_get.return_value = mock_response

    result = AeroplanesAPI().get_country_bounds("Canada")

    assert result == (10.0, 30.0, 20.0, 40.0)
    mock_response.raise_for_status.assert_called_once()


@patch("src.api.requests.get")
def test_country_not_found(mock_get):
    """Проверяет ошибку при отсутствии страны в ответе API."""
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Страна не найдена"):
        AeroplanesAPI().get_country_bounds("Canada")


@patch("src.api.requests.get")
def test_country_without_coordinates(mock_get):
    """Проверяет ошибку при отсутствии координат страны."""
    mock_response = Mock()
    mock_response.json.return_value = [{"display_name": "Canada"}]
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="не найдены координаты"):
        AeroplanesAPI().get_country_bounds("Canada")


@patch("src.api.requests.get")
def test_api_error(mock_get):
    """Проверяет передачу ошибки HTTP-запроса вызывающему коду."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = RequestException("API error")
    mock_get.return_value = mock_response

    with pytest.raises(RequestException):
        AeroplanesAPI().get_country_bounds("Canada")


@patch("src.api.requests.get")
def test_get_aeroplanes(mock_get):
    """Проверяет получение списка самолётов из ответа API."""
    api = AeroplanesAPI()
    api.get_country_bounds = Mock(return_value=(10.0, 30.0, 20.0, 40.0))

    mock_response = Mock()
    mock_response.json.return_value = {"states": [["abc123"], ["def456"]]}
    mock_get.return_value = mock_response

    result = api.get_aeroplanes("Canada")

    assert result == [["abc123"], ["def456"]]
    mock_response.raise_for_status.assert_called_once()


@patch("src.api.requests.get")
def test_get_aeroplanes_without_states(mock_get):
    """Проверяет возврат пустого списка при отсутствии самолётов."""
    api = AeroplanesAPI()
    api.get_country_bounds = Mock(return_value=(10.0, 30.0, 20.0, 40.0))

    mock_response = Mock()
    mock_response.json.return_value = {"states": None}
    mock_get.return_value = mock_response

    assert api.get_aeroplanes("Canada") == []
