from BackEnd.GameObjects.Robal import *
from Util.DirectionEnum import Direction

directionOptions = [Direction.WN, Direction.W, Direction.WS, Direction.ES, Direction.E, Direction.EN]
resourceFieldCoordinates = [[1, 0, -1], [-2, 3, -1], [1, -3, 2]]
board_size = 4


bug_types = ['K', 'M', 'P', 'Z']
bug_classes = {
            'K': Konik,
            'M': Mrowka,
            'P': Pajak,
            'Z': Zuk
}