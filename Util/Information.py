from BackEnd.GameObjects.Robal import *
from Util.DirectionEnum import Direction
from enum import IntEnum

directionOptions = [Direction.WN, Direction.W, Direction.WS, Direction.ES, Direction.E, Direction.EN]
resourceFieldCoordinates = [[-1, 3, -2], [0, 0, 0], [1, -3, 2]]
board_size = 4
n_tiles = 61
board_array_size = 2 * board_size + 1
bug_types = [RobalEnum.K, RobalEnum.M, RobalEnum.P, RobalEnum.Z]
bug_classes = {
    RobalEnum.K: Konik,
    RobalEnum.M: Mrowka,
    RobalEnum.P: Pajak,
    RobalEnum.Z: Zuk
}
banned_tiles = [(-1, 0)]


class ActionType(IntEnum):
    PASS = 0
    KILL = 1
    MOVE = 2
    HATCH = 3
