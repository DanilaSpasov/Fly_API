import json

import pytest

from src.storage import AbstractStorage, JSONSaver


def test_abstract_storage_cannot_be_created():
    """Проверяет запрет создания абстрактного хранилища."""
    with pytest.raises(TypeError):
        AbstractStorage()


def test_json_saver_init(tmp_path):
    """Проверяет инициализацию JSON-хранилища."""
    file_path = tmp_path / "aeroplanes.json"

    storage = JSONSaver(str(file_path))

    assert storage.file_path == str(file_path)


def test_add_aeroplane(tmp_path, aeroplane):
    """Проверяет добавление самолёта в JSON-хранилище."""
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONSaver(str(file_path))

    storage.add_aeroplane(aeroplane)

    data = json.loads(file_path.read_text(encoding="utf-8"))
    assert data == [
        {
            "icao24": "abc123",
            "callsign": "TEST123",
            "origin_country": "Canada",
            "altitude": 1000.0,
            "on_ground": False,
            "velocity": 200.0,
        }
    ]


def test_get_all_aeroplanes(tmp_path, aeroplanes):
    """Проверяет получение всех самолётов из хранилища."""
    storage = JSONSaver(str(tmp_path / "aeroplanes.json"))
    for aeroplane in aeroplanes:
        storage.add_aeroplane(aeroplane)

    result = storage.get_aeroplanes()

    assert len(result) == 3


def test_get_aeroplanes_by_criteria(tmp_path, aeroplanes):
    """Проверяет выбор самолётов по заданным критериям."""
    storage = JSONSaver(str(tmp_path / "aeroplanes.json"))
    for aeroplane in aeroplanes:
        storage.add_aeroplane(aeroplane)

    result = storage.get_aeroplanes({"origin_country": "Canada", "on_ground": False})

    assert len(result) == 1
    assert result[0]["icao24"] == "abc123"


def test_delete_aeroplane(tmp_path, aeroplanes):
    """Проверяет удаление самолёта из хранилища."""
    storage = JSONSaver(str(tmp_path / "aeroplanes.json"))
    for aeroplane in aeroplanes:
        storage.add_aeroplane(aeroplane)

    storage.delete_aeroplane("def456")

    result = storage.get_aeroplanes()
    assert [item["icao24"] for item in result] == ["abc123", "ghi789"]


def test_read_missing_file(tmp_path):
    """Проверяет чтение данных при отсутствии файла."""
    storage = JSONSaver(str(tmp_path / "missing.json"))

    assert storage.get_aeroplanes() == []


@pytest.mark.parametrize("file_content", ["{broken", "{}", '[{"icao24": "a"}, 1]'])
def test_read_invalid_data(tmp_path, file_content):
    """Проверяет чтение некорректных данных из файла."""
    file_path = tmp_path / "aeroplanes.json"
    file_path.write_text(file_content, encoding="utf-8")
    storage = JSONSaver(str(file_path))

    assert storage.get_aeroplanes() == []


def test_read_file_error(tmp_path):
    """Проверяет обработку ошибки чтения файла."""
    storage = JSONSaver(str(tmp_path))

    with pytest.raises(OSError, match="Не удалось прочитать файл"):
        storage.get_aeroplanes()


def test_write_file_error(tmp_path):
    """Проверяет обработку ошибки записи файла."""
    storage = JSONSaver(str(tmp_path))

    with pytest.raises(OSError, match="Не удалось записать файл"):
        storage._write_data([])


def test_serialization_error_does_not_change_file(tmp_path):
    """Проверяет сохранность файла при ошибке сериализации."""
    file_path = tmp_path / "aeroplanes.json"
    file_path.write_text("[]", encoding="utf-8")
    storage = JSONSaver(str(file_path))

    with pytest.raises(TypeError):
        storage._write_data([{"bad_value": {1, 2}}])

    assert file_path.read_text(encoding="utf-8") == "[]"
