from abc import ABC, abstractmethod
from array import *


class Robal(ABC):
    lastID = 0

    @abstractmethod
    def __init__(self, side):
        self.move = 0
        self.attack = 0
        self.toughness = 0
        self.ID = 0
        self.armyID = 0
        self.side = side
        self.field = None

    def getID(self):    # pozbyć się ID
        return self.ID

    def getNewID(self):
        self.lastID = self.lastID + 1
        return self.lastID

    def setField(self, field):
        self.field = field

class Konik(Robal):

    def __init__(self, side):
        self.move = 3
        self.attack = 0
        self.toughness = array('i', [1])
        self.ID = Robal.getNewID(self)
        self.side = side


class Mrowka(Robal):

    def __init__(self, side):
        self.move = 4
        self.attack = 1
        self.toughness = array('i', [3, 4])
        self.ID = Robal.getNewID(self)
        self.side = side


class Pajak(Robal):

    def __init__(self, side):
        self.move = 4
        self.attack = 3
        self.toughness = array('i', [1, 2, 3])
        self.ID = Robal.getNewID(self)
        self.side = side


class Zuk(Robal):

    def __init__(self, side):
        self.move = 2
        self.attack = 5
        self.toughness = array('i', [4, 5, 6])
        self.ID = Robal.getNewID(self)
        self.side = side
