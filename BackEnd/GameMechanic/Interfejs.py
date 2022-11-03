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

    def performMove(self):
        choice = ""
        for bug in self.bugList:
            bug.reset_moves()
        while choice != "end":
            self.update()
            armies = self.GM.getArmies(self.side)
            moves = []
            for index_army in range(len(armies)):
                if armies[index_army].numberOfMoves <= 0:
                    continue
                if self.GM.UI is None:
                    moves += concatenate_moves([index_army], armies[index_army].getValidMoves())
                else:
                    moves += concatenate_moves(armies[index_army], armies.getValidMoves())
            moves.append("end")
            if len(moves) > 1:
                choice = self.getMove(moves)
            else:
                choice = "end"
            if choice != "end":
                army_index, direction = choice
                armies[army_index].performMove(direction)
        self.update()

    def oppositeSide(self):
        if self.side == "B":
            return "C"
        else:
            return "B"

    def performAttack(self):
        choice = ""
        while choice != "end":
            self.update()
            armies = self.GM.getArmies(self.oppositeSide())
            attacks = []
            for armies_index in range(len(armies)):
                if self.GM.UI is None:
                    attacks += concatenate_moves([armies_index], armies[armies_index].getAttacks())
                else:
                    attacks += armies
                    break
            attacks.append("end")
            if len(attacks) > 1:
                choice = self.getAttack(attacks)
            else:
                choice = "end"
            if choice != "end":
                index, attacked_army = choice
                armies[index].performeMove(attacked_army)
        self.update()

    def performHatchery(self):
        choice = ""
        while choice != "end" and self.GM.isAvailableSpaceForHatch(self.side):
            self.update()
            trader = Trader()
            possible_to_hatch = trader.getOptions(self.resources)
            hatchery_fields = []
            if self.side == "C":
                hatchery_fields = self.GM.board.blacksHatchery
            elif self.side == "B":
                hatchery_fields = self.GM.board.whitesHatchery

            options = []

            for i in range(len(hatchery_fields)):
                if hatchery_fields[i].bug is None:
                    if self.GM.UI is None:
                        options.append(i)
                    else:
                        options.append(hatchery_fields[i])

            possible_to_hatch = concatenate_moves(options, possible_to_hatch)
            possible_to_hatch.append("end")
            choice = self.getHatch(possible_to_hatch)
            if choice != "end":
                field, bug = choice
                bug, price = trader.buyBug(bug, self.resources, self.side)
                self.bugList.append(bug)
                self.resources -= price
                bug.moveBugTo(hatchery_fields[field])
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
