from abc import ABC, abstractmethod
from array import *

class Robal(ABC):

    lastID = 0

    @property
    @abstractmethod
    def cost(self):
        pass

    @property
    @abstractmethod
    def move(self):
        pass

    @property
    @abstractmethod
    def attack(self):
        pass

    @property
    @abstractmethod
    def toughness(self):
        pass

    @property
    @abstractmethod
    def ID(self):
        pass

    #@abstractmethod
    #def __init__(self):
    #    pass

    @abstractmethod
    def getID(self):
        return self.ID()

    def getNewID(self):
        self.lastID = self.lastID + 1
        return self.lastID


class Konik(Robal):

    cost = 1
    move = 3
    attack = 0
    toughness = array('i', [1])
    ID = Robal.getNewID()

class Mrowka(Robal):

    cost = 1
    move = 4
    attack = 1
    toughness = array('i', [3, 4])
    ID = Robal.getNewID()

class Pajak(Robal):

    cost = 2
    move = 4
    attack = 3
    toughness = array('i', [1, 2, 3])
    ID = Robal.getNewID()

class Zuk(Robal):

    cost = 3
    move = 2
    attack = 5
    toughness = array('i', [4, 5, 6])
    ID = Robal.getNewID()

