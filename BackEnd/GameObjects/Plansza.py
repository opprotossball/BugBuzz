from numpy.core.defchararray import upper, lower

from BackEnd.GameObjects.Pole import Pole
from BackEnd.GameObjects.Robal import *
from Util import Information
from Util.PlayerEnum import PlayerEnum


class Plansza:
    def __init__(self, size=4):
        self.iterList = []

        self.resources = []

        self.whitesHatchery = []
        self.blacksHatchery = []

        self.size = size

        self.plane = [[[0 for x in range(2 * size + 2)] for x in range(2 * size + 2)] for x in range(2 * size + 2)]
        ##TODO optimize self.plan. A lot of memory is wasted.

        for q in range(-size, size + 1):
            for r in range(max(-size, -size - q), min(size + 1, size + 1 - q)):
                s = - q - r
                pole = Pole(q, r, s, self.size)
                self.setField(q, r, s, pole)
                self.iterList.append(pole)
        for pole in self.iterList:
            q, r, s = pole.q, pole.r, pole.s
            self.addNeighbours(self.getField(q, r, s))
        self.root = self.getField(0, 0, 0)
        self.setHatchery()
        self.setResources()

        sorted(self.iterList, key=getKeyFor)

    def setField(self, q, r, s, field):
        self.plane[q + self.size][r + self.size][s + self.size] = field

    def getField(self, q, r, s):
        return self.plane[q + self.size][r + self.size][s + self.size]

    def addNeighbours(self, pole):
        if pole.r - 1 >= -self.size and pole.s + 1 < self.size + 1:
            pole.setES(self.getField(pole.q, pole.r - 1, pole.s + 1))
        if pole.r - 1 >= -self.size and pole.q + 1 < self.size + 1:
            pole.setWS(self.getField(pole.q + 1, pole.r - 1, pole.s))
        if pole.s - 1 >= -self.size and pole.r + 1 < self.size + 1:
            pole.setWN(self.getField(pole.q, pole.r + 1, pole.s - 1))
        if pole.s - 1 >= -self.size and pole.q + 1 < self.size + 1:
            pole.setW(self.getField(pole.q + 1, pole.r, pole.s - 1))
        if pole.q - 1 >= -self.size and pole.r + 1 < self.size + 1:
            pole.setEN(self.getField(pole.q - 1, pole.r + 1, pole.s))
        if pole.q - 1 >= -self.size and pole.s + 1 < self.size + 1:
            pole.setE(self.getField(pole.q - 1, pole.r, pole.s + 1))

    def setHatchery(self):
        pole = self.root
        while pole.E is not None:
            pole = pole.E
        pole.setHatchery(True, 2, PlayerEnum.B)
        pole.WS.setHatchery(True, 1, PlayerEnum.B)
        pole.WN.setHatchery(True, 3, PlayerEnum.B)
        self.whitesHatchery = [pole, pole.WS, pole.WN]

        pole = self.root
        while pole.W is not None:
            pole = pole.W
        pole.setHatchery(True, 2, PlayerEnum.C)
        pole.ES.setHatchery(True, 3, PlayerEnum.C)
        pole.EN.setHatchery(True, 1, PlayerEnum.C)
        self.blacksHatchery = [pole, pole.ES, pole.EN]

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
                clone.iterList[i].bug = self.iterList[i].bug.clone()
        return clone

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
        power = 0
        for index, field in enumerate(self.iterList):
            input += field.__hash__() + index * 3
        return input


def getKeyFor(Pole):
    return Pole.r * 60 - Pole.q
