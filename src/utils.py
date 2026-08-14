from src.models import Aeroplane


def parse_countries(countries_input: str) -> list[str]:
    """Преобразует строку со странами в список названий."""
    countries = []

    for country in countries_input.split(","):
        country = country.strip()

        if country:
            countries.append(country)

    return countries


def filter_aeroplanes_by_countries(
    aeroplanes: list[Aeroplane], countries: list[str]
) -> list[Aeroplane]:
    """Фильтрует самолёты по странам регистрации."""
    if not countries:
        return aeroplanes.copy()

    normalized_countries = []

    for country in countries:
        normalized_countries.append(country.casefold())

    filtered_aeroplanes = []

    for aeroplane in aeroplanes:
        if aeroplane.origin_country.casefold() in normalized_countries:
            filtered_aeroplanes.append(aeroplane)

    return filtered_aeroplanes


def get_top_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane], top_n: int
) -> list[Aeroplane]:
    """Возвращает заданное количество самых высоко летящих самолётов."""
    if isinstance(top_n, bool) or not isinstance(top_n, int):
        raise TypeError("Количество самолетов должно быть целым числом")

    if top_n <= 0:
        raise ValueError("Количество самолетов должно быть больше нуля")

    sorted_aeroplanes = sorted(
        aeroplanes,
        key=lambda aeroplane: aeroplane.altitude,
        reverse=True,
    )

    return sorted_aeroplanes[:top_n]
