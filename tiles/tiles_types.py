from enum import Enum, auto


class TilesTypes(Enum):
    static = auto()
    dinamic = auto()
    building = auto()
    lucky = auto()
    bowser_bridge = auto()
    final_flag = auto()
    castel = auto()
    castel_flag = auto()
    platform = auto()


class TilesStates(Enum):
    normal = auto()
    empty = auto()


class CoinsNumber(Enum):
    lucky = 1
    building = 10
