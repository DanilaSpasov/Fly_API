from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):
    @abstractmethod
    def get_country_bounds(self, country: str) -> tuple[float, float, float, float]:
        """Получает границы указанной страны."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[list]:
        """Получает информацию о самолётах над указанной страной."""
        pass


class AeroplanesAPI(AbstractAPI):
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def get_country_bounds(self, country: str) -> tuple[float, float, float, float]:
        params = {
            "country": country,
            "format": "jsonv2",
            "featureType": "country",
            "limit": 1,
        }
        response = requests.get(
            url=self.NOMINATIM_URL,
            params=params,
            headers={"User-Agent": "FlyAPI/0.1 educational project"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"Страна не найдена: {country}")

        boundingbox = data[0].get("boundingbox")

        if not boundingbox:
            raise ValueError(f"Для страны {country} не найдены координаты")

        return (
            float(boundingbox[0]),
            float(boundingbox[2]),
            float(boundingbox[1]),
            float(boundingbox[3]),
        )

    def get_aeroplanes(self, country: str) -> list[list]:
        lamin, lomin, lamax, lomax = self.get_country_bounds(country)
        params = {
            "lamin": lamin,
            "lomin": lomin,
            "lamax": lamax,
            "lomax": lomax,
        }
        response = requests.get(
            url=self.OPENSKY_URL,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        states = data.get("states")
        return states or []
