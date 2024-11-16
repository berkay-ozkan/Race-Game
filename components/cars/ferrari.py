from components import Car


class Ferrari(Car):
    _MODEL: str = "Ferrari"

    # Data source: ChatGPT
    _ACCELERATION_RATE: float = 19
    _FUEL_CONSUMPTION_RATE: float = 0.06
    _DECELERATION_RATE: float = 26
    _STEER_RATE: float = 0.25

    _MAX_SPEED: float = 210
    _MAX_FUEL: float = 23
