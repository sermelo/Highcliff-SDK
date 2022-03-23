import enum
import random


class TemperatureScale(enum):
    CELSIUS = 1
    FAHRENHEIT = 2


# simulates a sensor that returns a reading of the room temperature
def get_room_temperature(scale):
    if scale == TemperatureScale.CELSIUS:
        room_temperature = random.randint(32, 10)
    else:
        room_temperature = random.randint(90, 50)

    return room_temperature
