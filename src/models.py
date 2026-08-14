class Aeroplane:
    icao24: str
    callsign: str
    origin_country: str
    altitude: float
    on_ground: bool
    velocity: float

    def __init__(
        self,
        icao24: str,
        callsign: str,
        origin_country: str,
        altitude: float,
        on_ground: bool,
        velocity: float,
    ) -> None:
        if isinstance(altitude, bool) or not isinstance(altitude, (int, float)):
            raise TypeError("Высота должна быть числом")

        if isinstance(velocity, bool) or not isinstance(velocity, (int, float)):
            raise TypeError("Скорость должна быть числом")

        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")

        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.__altitude = altitude
        self.on_ground = on_ground
        self.__velocity = velocity

    @property
    def altitude(self) -> float:
        return self.__altitude

    @property
    def velocity(self) -> float:
        return self.__velocity

    def is_faster_than(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только самолёты")
        return self.velocity > other.velocity

    def is_higher_than(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только самолёты")
        return self.altitude > other.altitude

    @classmethod
    def from_state(cls, data: list) -> "Aeroplane":
        aeroplane = cls(
            icao24=data[0],
            callsign=data[1].strip() if data[1] else "Неизвестно",
            origin_country=data[2],
            altitude=data[7],
            on_ground=data[8],
            velocity=data[9],
        )
        return aeroplane

    @classmethod
    def cast_to_object_list(cls, data: list) -> list["Aeroplane"]:
        result = []

        for item in data:
            if len(item) < 10:
                continue
            if item[7] is not None and item[9] is not None:
                result.append(cls.from_state(item))

        return result

    def __str__(self) -> str:
        return (
            f"Позывной: {self.callsign}, "
            f"страна регистрации: {self.origin_country}, "
            f"скорость: {self.velocity} м/с, "
            f"высота: {self.altitude} м."
        )
