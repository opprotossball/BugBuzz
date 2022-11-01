from numpy.core.defchararray import upper, lower

from BackEnd.Robal import Konik, Mrowka, Pajak, Zuk

from BackEnd.Pole import Pole


class Plansza:
    def __init__(self, size=4):
        self.plane = [[[0 for x in range(2 * size + 1)] for x in range(2 * size + 1)] for x in range(2 * size + 1)]
        ##TODO optimize self.plan. A lot of memory is wasted.
        self.iterList = []
        self.queue = []

        self.resources = []

        self.whitesHatchery = []
        self.blacksHatchery = []

        self.size = size
        for q in range(0, 2 * size + 1):
            for r in range(0, 2 * size + 1):
                for s in range(0, 2 * size + 1):
                    if (q + r + s - 3 * size == 0):
                        pole = Pole(q, r, s, self.size)
                        self.plane[q][r][s] = pole
                        self.queue.append([q, r, s])
                        self.iterList.append(pole)
        self.numberOfPole = len(self.queue)
        while len(self.queue) > 0:
            q, r, s = self.queue.pop(0)
            self.addNeighbours(self.plane[q][r][s])
        self.root = self.plane[size][size][size]
        self.setHatchery()
        self.setRecources()

        sorted(self.iterList, key=getKeyFor)

    def addNeighbours(self, pole):
        size = self.size
        if pole.r - 1 >= 0 and pole.s + 1 < size * 2 + 1:
            pole.setES(self.plane[pole.q][pole.r - 1][pole.s + 1])
        if pole.r - 1 >= 0 and pole.q + 1 < size * 2 + 1:
            pole.setWS(self.plane[pole.q + 1][pole.r - 1][pole.s])
        if pole.s - 1 >= 0 and pole.r + 1 < size * 2 + 1:
            pole.setWN(self.plane[pole.q][pole.r + 1][pole.s - 1])
        if pole.s - 1 >= 0 and pole.q + 1 < size * 2 + 1:
            pole.setW(self.plane[pole.q + 1][pole.r][pole.s - 1])
        if pole.q - 1 >= 0 and pole.r + 1 < size * 2 + 1:
            pole.setEN(self.plane[pole.q - 1][pole.r + 1][pole.s])
        if pole.q - 1 >= 0 and pole.s + 1 < size * 2 + 1:
            pole.setE(self.plane[pole.q - 1][pole.r][pole.s + 1])

    def setHatchery(self):
        pole = self.root
        while pole.E is not None:
            pole = pole.E
        pole.setHatchery(True, 2)
        pole.WS.setHatchery(True, 1)
        pole.WN.setHatchery(True, 3)
        self.whitesHatchery = [pole, pole.WS, pole.WN]

        pole = self.root
        while pole.W is not None:
            pole = pole.W
        pole.setHatchery(True, 2)
        pole.ES.setHatchery(True, 3)
        pole.EN.setHatchery(True, 1)
        self.blacksHatchery = [pole, pole.ES, pole.EN]

    def setRecources(self):
        pola = [[1 + self.size, 0 + self.size, -1 + self.size], [-2 + self.size, 3 + self.size, -1 + self.size],
                [1 + self.size, -3 + self.size, 2 + self.size]]
        for pole in self.iterList:
            if pole.cor() in pola:
                pole.setResources(True)
                self.resources.append(pole)

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
                input += 0*pow(16, power)
            elif field.bug.short_name == 'k' and field.bug.side == "B":
                input += 1*pow(16, power)
            elif field.bug.short_name == 'm' and field.bug.side == "B":
                input += 2*pow(16, power)
            elif field.bug.short_name == 'p' and field.bug.side == "B":
                input += 3*pow(16, power)
            elif field.bug.short_name == 'z' and field.bug.side == "B":
                input += 4*pow(16, power)
            elif field.bug.short_name == 'k' and field.bug.side == "C":
                input += 9*pow(16, power)
            elif field.bug.short_name == 'm' and field.bug.side == "C":
                input += 10*pow(16, power)
            elif field.bug.short_name == 'p' and field.bug.side == "C":
                input += 11*pow(16, power)
            elif field.bug.short_name == 'z' and field.bug.side == "C":
                input += 12*pow(16, power)
            power += 1
        return input


def getKeyFor(Pole):
    return Pole.r * 60 - Pole.q
