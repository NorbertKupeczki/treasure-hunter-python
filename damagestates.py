from enum import IntEnum


class DamageStates(IntEnum):
    HEALTHY = 0
    DAMAGED = 1
    VERY_DAMAGED = 2
    NEAR_DEAD = 3
    DEAD = 4