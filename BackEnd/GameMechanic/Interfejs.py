from abc import ABC, abstractmethod

from BackEnd.GameObjects.Trader import Trader


def concatenate_moves(table1, table2):
    concatenated = []
    for el1 in table1:
        for el2 in table2:
            concatenated.append((el1, el2))
    return concatenated


class Interfejs(ABC):
    def __init__(self, GM, side, updateMethod):
        self.side = side
        self.resources = 0
        self.GM = GM

        self.update = updateMethod

        self.bugList = []

        self.hatchery = []

    def performMove(self):
        choice = ""
        armies = self.GM.getArmies(self)
        self.GM.reset_move_left(armies)
        while choice != "end":
            moves = self.GM.getMovesForPlayer(self)
            if len(moves) > 1:
                choice = self.getMove(moves)
            else:
                choice = "end"

            if choice != "end":
                army, direction = choice
                self.GM.performMove(army, direction)
            self.update()

    def performAttack(self):
        choice = ""
        while choice != "end":
            self.update()
            attacks = self.GM.getAttacksForPlayer(self)

            if len(attacks) > 1:
                choice = self.getAttack(attacks)
            else:
                choice = "end"

            if choice != "end":
                attacked_army = choice
                self.GM.performAttack1(attacked_army)
            self.update()

    def performHatchery(self):
        choice = ""
        self.resources = self.GM.getResourcesForPlayer(self)
        while choice != "end":
            self.update()
            possible_to_hatch = self.GM.getHatchForPlayer(self)

            if len(possible_to_hatch) > 1:
                choice = self.getHatch(possible_to_hatch)
            else:
                choice = "end"

            if choice != "end":
                field, bug = choice
                self.GM.performHatch(self, field, bug)
            self.update()

    @abstractmethod
    def getMove(self, possible_moves):
        pass

    @abstractmethod
    def getAttack(self, possible_attacks):
        pass

    @abstractmethod
    def getHatch(self, possible_hatch):
        pass
