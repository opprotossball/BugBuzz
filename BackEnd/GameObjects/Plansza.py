from numpy.core.defchararray import upper, lower

from BackEnd.GameObjects.Pole import Pole
from BackEnd.GameObjects.Robal import *
from Util import Information
from Util.Information import Direction
from Util.PlayerEnum import PlayerEnum


class Plansza:
    def __init__(self, size=4):
        self.iterList = []

        self.resources = []

        self.whitesHatchery = []
        self.blacksHatchery = []

        self.size = size

        self.plane = [[0 for x in range(2 * size + 1)] for x in range(2 * size + 1)]

        for x in range(-size, size + 1):
            for y in range(max(-size, -size - x), min(size + 1, size + 1 - x)):
                pole = Pole(x, y, - x - y, self.size, self)
                self.setField(pole, x, y)
                self.iterList.append(pole)

        self.root = self.getField(0, 0, 0)

        self.setHatchery()
        self.setResources()

        sorted(self.iterList, key=getKeyFor)

    def setField(self,  field, x, y, s=0):
        try:
            self.plane[y + self.size][x + self.size] = field
        except IndexError:
            return None

    def getField(self, x, y, s=0):
        try:
            val = self.plane[y + self.size][x + self.size]
            if val == 0:
                return None
            return val
        except IndexError:
            return None

    def is_valid_neigh(self, pole, dir):
        if dir == Direction.ES:
            return pole.y + 1 <= self.size
        elif dir == Direction.WS:
            return pole.x - 1 >= -self.size and pole.y + 1 <= self.size
        elif dir == Direction.WN:
            return pole.y - 1 >= -self.size
        elif dir == Direction.W:
            return pole.x - 1 >= -self.size
        elif dir == Direction.EN:
            return pole.x + 1 <= self.size and pole.y - 1 >= -self.size
        elif dir == Direction.E:
            return pole.x + 1 <= self.size
        return False

    def get_field_neighs(self, pole):
        neighs = []
        for dir in Information.directionOptions:
            neighs.append(self.get_field_neigh(pole, dir))

        return neighs

    def get_field_neigh(self, pole, dir):
        if dir == Direction.ES:
            return self.getField(pole.x, pole.y + 1)
        elif dir == Direction.WS:
            return self.getField(pole.x - 1, pole.y + 1)
        elif dir == Direction.WN:
            return self.getField(pole.x, pole.y - 1)
        elif dir == Direction.W:
            return self.getField(pole.x - 1, pole.y)
        elif dir == Direction.EN:
            return self.getField(pole.x + 1, pole.y - 1)
        elif dir == Direction.E:
            return self.getField(pole.x + 1, pole.y)
        return None


    def setHatchery(self):
        pole = self.getField(0, 0, 0)
        while self.is_valid_neigh(pole, Direction.E):
            pole = self.get_field_neigh(pole, Direction.E)
        pole2 = pole
        pole1 = self.get_field_neigh(pole, Direction.WS)
        pole3 = self.get_field_neigh(pole, Direction.WN)

        pole2.setHatchery(2, PlayerEnum.C)
        pole3.setHatchery(3, PlayerEnum.C)
        pole1.setHatchery(1, PlayerEnum.C)
        self.blacksHatchery = [pole1, pole2, pole3]

        pole = self.getField(0, 0, 0)
        while self.is_valid_neigh(pole, Direction.W):
            pole = self.get_field_neigh(pole, Direction.W)
        pole2 = pole
        pole1 = self.get_field_neigh(pole, Direction.ES)
        pole3 = self.get_field_neigh(pole, Direction.EN)

        pole2.setHatchery(2, PlayerEnum.B)
        pole1.setHatchery(1, PlayerEnum.B)
        pole3.setHatchery(3, PlayerEnum.B)
        self.whitesHatchery = [pole3, pole1, pole2]

    def setResources(self):
        fields_cor = Information.resourceFieldCoordinates
        for cor in fields_cor:
            field = self.getField(cor[0], cor[1], cor[2])
            field.setResources(True)
            self.resources.append(field)

    def clone(self):
        clone = Plansza(self.size)
        for i in range(len(self.iterList)):
            if self.iterList[i].bug is not None:
                bug = self.iterList[i].bug.clone()
                bug.moveBugTo(clone.iterList[i])
        return clone

    def get_hatchery(self, side):
        if side == 'B':
            return self.whitesHatchery
        else:
            return self.blacksHatchery

    def getPositionWithoutToMoveNorResourcesInfo(self):
        position = ''
        for i in self.iterList:
            if i.bug is None:
                position += '.'
            else:
                if i.bug.side == PlayerEnum.B:
                    position += upper(i.bug.short_name)
                elif i.bug.side == PlayerEnum.C:
                    position += lower(i.bug.short_name)
        return position

    def loadPosition(self, position):
        for actual_field, position_content in zip(self.iterList, position):
            if position_content == "K":
                actual_field.bug = Konik(PlayerEnum.B)
            elif position_content == "M":
                actual_field.bug = Mrowka(PlayerEnum.B)
            elif position_content == "P":
                actual_field.bug = Pajak(PlayerEnum.B)
            elif position_content == "Z":
                actual_field.bug = Zuk(PlayerEnum.B)
            elif position_content == "k":
                actual_field.bug = Konik(PlayerEnum.C)
            elif position_content == "m":
                actual_field.bug = Mrowka(PlayerEnum.C)
            elif position_content == "p":
                actual_field.bug = Pajak(PlayerEnum.C)
            elif position_content == "z":
                actual_field.bug = Zuk(PlayerEnum.C)

    def getInput(self):
        input = []
        for field in self.iterList:
            input += field.toCode()
        return input

    def __hash__(self):
        input = 0
        for index, field in enumerate(self.iterList):
            input += field.__hash__() + index * 3
        return input


def getKeyFor(Pole):
    return Pole.y * 60 - Pole.x
