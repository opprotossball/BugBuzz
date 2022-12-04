from abc import ABC, abstractmethod
from array import *
from enum import Enum


class RobalEnum(Enum):
    K = 0
    M = 1
    P = 2
    Z = 3

class States(Enum):
    Moved = 0
    ToMove = 1
    WontMove = 2

class Robal(ABC):
    lastID = 0

    @abstractmethod
    def __init__(self, side):
        self.move = 0
        self.attack = 0
        self.toughness = []
        self.cost = 0
        self.army = None
        self.side = side
        self.field = None

        self.short_name = ""
        self.validMoves = []
        self.invalidMoves = []
        self.moveToExamine = []

        self.moved = False


    def recruitNeighbours(self):
        for field in self.field.getNeighbours():
            if field is not None and field.bug is not None and field.bug.side == self.side and field.bug.army is None:
                self.army.addBug(field.bug)
                field.bug.recruitNeighbours()
        self.state = States.Moved

    def setField(self, field):
        self.field = field

    def moveBugTo(self, field):
        if self.field is not None:
            self.field.bug = None
        self.field = field
        self.field.bug = self

    def clone(self):
        clone = self.__class__(self.side)
        clone.move = self.move
        return clone

    def clone_with_field(self):
        clone = self.__class__(self.side)
        clone.field = self.field
        clone.move = self.move
        return clone

    def hasEnemyInSurrounding(self):
        fields = self.field.board.get_field_neighs(self.field)
        for field in fields:
            if field is not None and field.bug is not None and field.bug.side != self.side:
                return True
        return False

    def setMove(self, move):
        self.move = move


class Konik(Robal):

    def __init__(self, side):
        self.cost = 1
        self.max_move = 3
        self.move = 3
        self.attack = 0
        self.toughness = [1]
        self.side = side
        self.army = None
        self.field = None
        self.short_name = RobalEnum.K
        self.validMoves = []
        self.invalidMoves = []
        self.moveToExamine = []
        self.moved = False


class Mrowka(Robal):

    def __init__(self, side):
        self.cost = 1
        self.max_move = 4
        self.move = 4
        self.attack = 1
        self.toughness = [3, 4]
        self.side = side
        self.army = None
        self.field = None
        self.short_name = RobalEnum.M
        self.validMoves = []
        self.invalidMoves = []
        self.moveToExamine = []
        self.moved = False


class Pajak(Robal):

    def __init__(self, side):
        self.cost = 2
        self.max_move = 4
        self.move = 4
        self.attack = 3
        self.toughness = [1, 2, 3]
        self.side = side
        self.army = None
        self.field = None
        self.short_name = RobalEnum.P
        self.validMoves = []
        self.invalidMoves = []
        self.moveToExamine = []
        self.moved = False


class Zuk(Robal):

    def __init__(self, side):
        self.cost = 3
        self.max_move = 2
        self.move = 2
        self.attack = 5
        self.toughness = [4, 5, 6]
        self.side = side
        self.army = None
        self.field = None
        self.short_name = RobalEnum.Z
        self.validMoves = []
        self.invalidMoves = []
        self.moveToExamine = []
        self.moved = False
