from enum import Enum, auto


class PlayerColors(Enum):
    red = auto()
    green = auto()


class InputActions(Enum):
    jump = auto()
    duck = auto()
    left = auto()
    right = auto()
    sprint = auto()
    pause = auto()
    slow_game = auto()


class EventAnimationsTypes(Enum):
    lvup = auto()
    flower = auto()
    star = auto()
    damage = auto()


class Cutscenes(Enum):
    flag = auto()
    tube = auto()


class PlayerStates(Enum):
    little = auto()
    big = auto
    flower = auto()


class DefaultAnimationCategories(Enum):
    normal = auto()
    firing = auto()


class MovementTypes(Enum):
    standing = auto()
    ducking = auto()
    walking = auto()
    running = auto()
    skiding = auto()
    jumping = auto()
    swiming = auto()
    climbing = auto()
    declining = auto()
