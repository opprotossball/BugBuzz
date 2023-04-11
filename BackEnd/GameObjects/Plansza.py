from BackEnd.GameObjects.Pole import Pole
from Util import Information
from Util.Information import Direction
from Util.PlayerEnum import PlayerEnum


class Plansza:
    def __init__(self, size=4, banned_tiles=None):
        self.iterList = []

        self.resources = []

        self.whitesHatchery = []
        self.blacksHatchery = []

        self.size = size

        self.plane = [[0 for _ in range(2 * size + 1)] for _ in range(2 * size + 1)]

        for x in range(-size, size + 1):
            for y in range(max(-size, -size - x), min(size + 1, size + 1 - x)):
                pole = Pole(x, y, - x - y, self.size, self)
                self.set_field(pole, x, y)
                self.iterList.append(pole)
        self.root = self.get_field(0, 0, 0)

        self.set_hatchery()
        self.set_resources()

        sorted(self.iterList, key=get_key_for)

        if banned_tiles is not None:
            for b in banned_tiles:
                self.get_field(b[0], b[1]).banned = True

    def set_field(self, field, x, y, s=0):
        try:
            self.plane[y + self.size][x + self.size] = field
        except IndexError:
            return None

    def get_field(self, x, y, s=0):
        if y + self.size < 0 or x + self.size < 0:
            return None
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
            return self.get_field(pole.x, pole.y + 1)
        elif dir == Direction.WS:
            return self.get_field(pole.x - 1, pole.y + 1)
        elif dir == Direction.WN:
            return self.get_field(pole.x, pole.y - 1)
        elif dir == Direction.W:
            return self.get_field(pole.x - 1, pole.y)
        elif dir == Direction.EN:
            return self.get_field(pole.x + 1, pole.y - 1)
        elif dir == Direction.E:
            return self.get_field(pole.x + 1, pole.y)
        return None

    def set_hatchery(self):
        pole = self.get_field(0, 0, 0)
        while self.is_valid_neigh(pole, Direction.E):
            pole = self.get_field_neigh(pole, Direction.E)
        pole2 = pole
        pole1 = self.get_field_neigh(pole, Direction.WS)
        pole3 = self.get_field_neigh(pole, Direction.WN)

        pole2.set_hatchery(2, PlayerEnum.C)
        pole3.set_hatchery(3, PlayerEnum.C)
        pole1.set_hatchery(1, PlayerEnum.C)
        self.blacksHatchery = [pole1, pole2, pole3]

        pole = self.get_field(0, 0, 0)
        while self.is_valid_neigh(pole, Direction.W):
            pole = self.get_field_neigh(pole, Direction.W)
        pole2 = pole
        pole1 = self.get_field_neigh(pole, Direction.ES)
        pole3 = self.get_field_neigh(pole, Direction.EN)

        pole2.set_hatchery(2, PlayerEnum.B)
        pole1.set_hatchery(1, PlayerEnum.B)
        pole3.set_hatchery(3, PlayerEnum.B)
        self.whitesHatchery = [pole3, pole1, pole2]

    def set_resources(self):
        fields_cor = Information.resourceFieldCoordinates
        for cor in fields_cor:
            field = self.get_field(cor[0], cor[1], cor[2])
            field.set_resources(True)
            self.resources.append(field)

    def clone(self):
        clone = Plansza(self.size)
        for i in range(len(self.iterList)):
            if self.iterList[i].bug is not None:
                bug = self.iterList[i].bug.clone()
                bug.move_bug_to(clone.iterList[i])
        return clone

    def get_hatchery(self, side):
        if side == PlayerEnum.B:
            return self.whitesHatchery
        else:
            return self.blacksHatchery


def get_key_for(Pole):
    return Pole.y * 60 - Pole.x
