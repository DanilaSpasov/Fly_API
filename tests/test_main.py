from unittest.mock import Mock
from unittest.mock import patch

from requests import RequestException

import main


@patch("builtins.input", return_value="5")
def test_get_top_n_from_user(mock_input):
    """Проверяет получение положительного числа от пользователя."""
    assert main.get_top_n_from_user() == 5


@patch("builtins.input", side_effect=["text", "0", "2"])
def test_get_top_n_wrong_input(mock_input, capsys):
    """Проверяет повторный запрос при некорректном пользовательском вводе."""
    result = main.get_top_n_from_user()
    output = capsys.readouterr().out

    assert result == 2
    assert "должно быть целым числом" in output
    assert "должно быть больше нуля" in output


def test_print_aeroplanes(aeroplane, capsys):
    """Проверяет вывод заголовка и данных о самолёте."""
    main.print_aeroplanes("Список самолетов:", [aeroplane])

    output = capsys.readouterr().out
    assert "Список самолетов:" in output
    assert "Позывной: TEST123" in output


def test_print_empty_aeroplanes(capsys):
    """Проверяет сообщение при выводе пустого списка самолётов."""
    main.print_aeroplanes("Список самолетов:", [])

    output = capsys.readouterr().out
    assert "Самолеты не найдены." in output


@patch("builtins.input", return_value="")
def test_user_interaction_empty_country(mock_input, capsys):
    """Проверяет обработку пустого названия страны."""
    main.user_interaction()

    assert "Название страны не может быть пустым" in capsys.readouterr().out


@patch("builtins.input", return_value="Canada")
@patch("main.AeroplanesAPI")
def test_user_interaction_api_error(mock_api_class, mock_input, capsys):
    """Проверяет сообщение пользователю при ошибке API."""
    mock_api = Mock()
    mock_api.get_aeroplanes.side_effect = RequestException("API error")
    mock_api_class.return_value = mock_api

    main.user_interaction()

    assert "Не удалось получить данные от API" in capsys.readouterr().out


@patch("builtins.input", return_value="Canada")
@patch("main.AeroplanesAPI")
def test_user_interaction_without_aeroplanes(mock_api_class, mock_input, capsys):
    """Проверяет сообщение при отсутствии самолётов в стране."""
    mock_api = Mock()
    mock_api.get_aeroplanes.return_value = []
    mock_api_class.return_value = mock_api

    main.user_interaction()

    assert "не найдены" in capsys.readouterr().out
