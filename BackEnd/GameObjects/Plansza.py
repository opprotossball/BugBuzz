from numpy.core.defchararray import upper, lower

from BackEnd.GameObjects.Robal import Konik, Mrowka, Pajak, Zuk

from BackEnd.GameObjects.Pole import Pole
from Util import Information


class Plansza:
    def __init__(self, size=4):
        self.iterList = []

        self.resources = []

        self.whitesHatchery = []
        self.blacksHatchery = []

        self.size = size

        self.plane = [[0 for x in range(2 * size + 1)] for x in range(2 * size + 1)]

        for q in range(-size, size + 1):
            for r in range(max(-size, -size-q), min(size + 1, size + 1 - q)):
                s = - q - r
                pole = Pole(q, r, s, self.size)
                self.setField (q, r, s, pole)
                self.iterList.append(pole)

        for pole in self.iterList:
            self.addNeighbours(pole)

        self.root = self.getField(0, 0, 0)

        self.setHatchery()
        self.setResources()

        sorted(self.iterList, key=getKeyFor)

    def setField(self, q, r, s, field):
        self.plane[q + self.size][r + self.size] = field

    def getField(self, q, r, s):
        return self.plane[q + self.size][r + self.size]

    def addNeighbours(self, pole):
        if pole.r - 1 >= -self.size and pole.s < self.size:
            pole.setES(self.getField(pole.q, pole.r - 1, pole.s + 1))
        if pole.r - 1 >= -self.size and pole.q < self.size:
            pole.setWS(self.getField(pole.q + 1, pole.r - 1, pole.s))
        if pole.s - 1 >= -self.size and pole.r < self.size:
            pole.setWN(self.getField(pole.q, pole.r + 1, pole.s - 1))
        if pole.s - 1 >= -self.size and pole.q < self.size:
            pole.setW(self.getField(pole.q + 1, pole.r, pole.s - 1))
        if pole.q - 1 >= -self.size and pole.r < self.size:
            pole.setEN(self.getField(pole.q - 1, pole.r + 1, pole.s))
        if pole.q - 1 >= -self.size and pole.s < self.size:
            pole.setE(self.getField(pole.q - 1, pole.r, pole.s + 1))

    def setHatchery(self):
        pole = self.root
        while pole.E is not None:
            pole = pole.E
        pole.setHatchery(True, 2, "B")
        pole.WS.setHatchery(True, 1, "B")
        pole.WN.setHatchery(True, 3, "B")
        self.whitesHatchery = [pole, pole.WS, pole.WN]

        pole = self.root
        while pole.W is not None:
            pole = pole.W
        pole.setHatchery(True, 2, "C")
        pole.ES.setHatchery(True, 3, "C")
        pole.EN.setHatchery(True, 1, "C")
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
                if i.bug.side == "B":
                    position += upper(i.bug.short_name)
                elif i.bug.side == "C":
                    position += lower(i.bug.short_name)
        return position

    def loadPosition(self, position):
        for actual_field, position_content in zip(self.iterList, position):
            if position_content == "K":
                actual_field.bug = Konik("B")
            elif position_content == "M":
                actual_field.bug = Mrowka("B")
            elif position_content == "P":
                actual_field.bug = Pajak("B")
            elif position_content == "Z":
                actual_field.bug = Zuk("B")
            elif position_content == "k":
                actual_field.bug = Konik("C")
            elif position_content == "m":
                actual_field.bug = Mrowka("C")
            elif position_content == "p":
                actual_field.bug = Pajak("C")
            elif position_content == "z":
                actual_field.bug = Zuk("C")

    def getInput(self):
        input = []
        for field in self.iterList:
            if field.bug is None:
                input += [0, 0, 0, 0]
            elif field.bug.short_name == 'k' and field.bug.side == "B":
                input += [0, 0, 0, 1]
            elif field.bug.short_name == 'm' and field.bug.side == "B":
                input += [0, 0, 1, 0]
            elif field.bug.short_name == 'p' and field.bug.side == "B":
                input += [0, 0, 1, 1]
            elif field.bug.short_name == 'z' and field.bug.side == "B":
                input += [0, 1, 0, 0]
            elif field.bug.short_name == 'k' and field.bug.side == "C":
                input += [1, 0, 0, 1]
            elif field.bug.short_name == 'm' and field.bug.side == "C":
                input += [1, 0, 1, 0]
            elif field.bug.short_name == 'p' and field.bug.side == "C":
                input += [1, 0, 1, 1]
            elif field.bug.short_name == 'z' and field.bug.side == "C":
                input += [1, 1, 0, 0]
        return input

    def __hash__(self):
        input = 0
        power = 0
        for field in self.iterList:
            if field.bug is None:
                input += 0
            elif field.bug.short_name == 'K' and field.bug.side == "B":
                input += 1*pow(16, power)
            elif field.bug.short_name == 'M' and field.bug.side == "B":
                input += 2*pow(16, power)
            elif field.bug.short_name == 'P' and field.bug.side == "B":
                input += 3*pow(16, power)
            elif field.bug.short_name == 'Z' and field.bug.side == "B":
                input += 4*pow(16, power)
            elif field.bug.short_name == 'K' and field.bug.side == "C":
                input += 9*pow(16, power)
            elif field.bug.short_name == 'M' and field.bug.side == "C":
                input += 10*pow(16, power)
            elif field.bug.short_name == 'P' and field.bug.side == "C":
                input += 11*pow(16, power)
            elif field.bug.short_name == 'Z' and field.bug.side == "C":
                input += 12*pow(16, power)
            power += 1
        return input

    def get_hash_2(self):
        empty_count = 0
        code = ""
        for t in self.iterList:
            if t.bug is None:
                empty_count += 1
            else:
                if empty_count != 0:
                    code += str(empty_count)
                    empty_count = 0
                name = t.bug.short_name
                if t.bug.side == "C":
                    name = name.lower()
                code += name
        return code.__hash__()

def getKeyFor(Pole):
    return Pole.get_key_for()
