from abc import ABC, abstractmethod
from array import *


class Robal(ABC):
    @abstractmethod
    def __init__(self, side):
        self.move = 0
        self.attack = 0
        self.toughness = 0
        self.army = None
        self.side = side
        self.field = None
        self.short_name = ""

    def setField(self, field):
        self.field = field


class Konik(Robal):

    def __init__(self, side):
        self.move = 3
        self.attack = 0
        self.toughness = array('i', [1])
        self.side = side
        self.short_name = "K"

class Mrowka(Robal):

    def __init__(self, side):
        self.move = 4
        self.attack = 1
        self.toughness = array('i', [3, 4])
        self.side = side
        self.short_name = "M"


class Pajak(Robal):

    def __init__(self, side):
        self.move = 4
        self.attack = 3
        self.toughness = array('i', [1, 2, 3])
        self.side = side
        self.short_name = "P"


class Zuk(Robal):

    def __init__(self, side):
        self.move = 2
        self.attack = 5
        self.toughness = array('i', [4, 5, 6])
        self.side = side
        self.short_name = "Z"
