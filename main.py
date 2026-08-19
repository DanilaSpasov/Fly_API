from requests import RequestException

from src.api import AeroplanesAPI
from src.models import Aeroplane
from src.storage import JSONSaver
from src.utils import (
    filter_aeroplanes_by_countries,
    get_top_aeroplanes_by_altitude,
    parse_countries,
)


def get_top_n_from_user() -> int:
    """Получает от пользователя количество самолётов для топа."""
    while True:
        top_n_input = input("Введите количество самолетов для топа: ").strip()

        try:
            top_n = int(top_n_input)
        except ValueError:
            print("Количество самолетов должно быть целым числом.")
            continue

        if top_n <= 0:
            print("Количество самолетов должно быть больше нуля.")
            continue

        return top_n


def print_aeroplanes(title: str, aeroplanes: list[Aeroplane]) -> None:
    """Выводит заголовок и список самолётов."""
    print(f"\n{title}")

    if not aeroplanes:
        print("Самолеты не найдены.")
        return

    for aeroplane in aeroplanes:
        print(aeroplane)


def user_interaction() -> None:
    """Запускает взаимодействие с пользователем."""
    country = input("Введите страну для поиска самолетов: ").strip()

    if not country:
        print("Название страны не может быть пустым.")
        return

    api = AeroplanesAPI()

    try:
        states = api.get_aeroplanes(country)
    except ValueError as error:
        print(error)
        return
    except RequestException as error:
        print(f"Не удалось получить данные от API: {error}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(states)

    if not aeroplanes:
        print(f"Самолеты в воздушном пространстве страны {country} не найдены.")
        return

    json_saver = JSONSaver("aeroplanes.json")

    try:
        for aeroplane in aeroplanes:
            json_saver.add_aeroplane(aeroplane)
    except (OSError, TypeError) as error:
        print(f"Не удалось сохранить данные о самолетах: {error}")
        return

    top_n = get_top_n_from_user()
    top_aeroplanes = get_top_aeroplanes_by_altitude(aeroplanes, top_n)

    countries_input = input("Введите страны регистрации через запятую: ")
    registration_countries = parse_countries(countries_input)
    filtered_aeroplanes = filter_aeroplanes_by_countries(
        aeroplanes,
        registration_countries,
    )

    print_aeroplanes(
        f"Топ-{top_n} самолетов по высоте:",
        top_aeroplanes,
    )
    print_aeroplanes(
        "Самолеты выбранных стран регистрации:",
        filtered_aeroplanes,
    )


if __name__ == "__main__":
    user_interaction()
