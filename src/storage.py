import json
from abc import ABC, abstractmethod

from src.models import Aeroplane


class AbstractStorage(ABC):
    """Определяет интерфейс хранилища самолётов."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Сохраняет данные о самолёте."""
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: dict | None = None) -> list[dict]:
        """Возвращает данные о самолётах по указанным критериям."""
        pass

    @abstractmethod
    def delete_aeroplane(self, icao24: str) -> None:
        """Удаляет данные о самолёте по идентификатору."""
        pass


class JSONSaver(AbstractStorage):
    """Сохраняет данные о самолётах в JSON-файле."""

    file_path: str

    def __init__(self, file_path: str) -> None:
        """Создаёт хранилище для указанного JSON-файла."""
        self.file_path = file_path

    def _read_data(self) -> list[dict]:
        """Читает данные о самолётах из JSON-файла."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if not isinstance(data, list):
                    return []

                if not all(isinstance(item, dict) for item in data):
                    return []

                return data
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
            return []
        except OSError as error:
            raise OSError(f"Не удалось прочитать файл: {self.file_path}") from error

    def _write_data(self, data: list[dict]) -> None:
        """Записывает данные о самолётах в JSON-файл."""
        json_text = json.dumps(data, ensure_ascii=False, indent=4)

        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(json_text)
        except OSError as error:
            raise OSError(f"Не удалось записать файл: {self.file_path}") from error

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Сохраняет данные о самолёте."""
        data = self._read_data()

        aeroplane_data = {
            "icao24": aeroplane.icao24,
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "altitude": aeroplane.altitude,
            "on_ground": aeroplane.on_ground,
            "velocity": aeroplane.velocity,
        }
        data.append(aeroplane_data)
        self._write_data(data)

    def get_aeroplanes(self, criteria: dict | None = None) -> list[dict]:
        """Возвращает данные о самолётах по указанным критериям."""
        data = self._read_data()

        if not criteria:
            return data

        result = []

        for aeroplane_data in data:
            matches = True

            for key, value in criteria.items():
                if aeroplane_data.get(key) != value:
                    matches = False
                    break

            if matches:
                result.append(aeroplane_data)

        return result

    def delete_aeroplane(self, icao24: str) -> None:
        """Удаляет данные о самолёте по идентификатору."""
        data = self._read_data()
        remaining_aeroplanes = []

        for aeroplane_data in data:
            if aeroplane_data.get("icao24") != icao24:
                remaining_aeroplanes.append(aeroplane_data)

        self._write_data(remaining_aeroplanes)
