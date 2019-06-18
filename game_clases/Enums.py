from enum import Enum

class Directions(Enum):
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)
