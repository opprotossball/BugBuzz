from BackEnd.Trader import Trader


def concatenate_moves(table1, table2):
    concatenated = []
    for el1 in table1:
        for el2 in table2:
            concatenated.append((el1, el2))
    return concatenated


class Interfejs:
    def __init__(self, GM, side, updateMethod):
        self.side = side
        self.resources = 0
        self.GameMaster = GM

        self.update = updateMethod

        self.bugList = []

    def performMove(self):
        choice = ""
        while choice != "end":
            self.update()
            armies = self.GameMaster.getArmies(self.side)
            moves = []
            for index_army in range(len(armies)):
                if armies[index_army].numberOfMoves == 0:
                    continue
                moves += concatenate_moves([index_army], armies[index_army].getValidMoves())
            moves.append("end")
            choice = self.getMove(moves)
            if choice != "end":
                army_index, direction = choice
                armies[army_index].performMove(direction)
        self.update()

    def performAttack(self):
        choice = ""
        while choice != "end":
            self.update()
            armies = self.GameMaster.getArmies(self.side)
            attacks = []
            for i in range(len(armies)):
                attacks += concatenate_moves([i], armies[i].getAttacks())
            attacks.append("end")
            choice = self.getAttack(attacks)
            if choice != "end":
                index, attacked_army = choice
                armies[index].performeMove(attacked_army)
        self.update()

    def performHatchery(self):
        choice = ""
        while choice != "end" and self.GameMaster.isAvailableSpaceForHatch(self.side):
            self.update()
            trader = Trader()
            possible_to_hatch = trader.getOptions(self.resources)
            hatchery_fields = []
            if self.side == "C":
                hatchery_fields = self.GameMaster.plansza.blacksHatchery
            elif self.side == "B":
                hatchery_fields = self.GameMaster.plansza.whitesHatchery

            options = []

            for i in range(len(hatchery_fields)):
                if hatchery_fields[i].bug is None:
                    options.append(i)

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

    # abstract
    def getMove(self, possible_moves):
        pass

    # abstract
    def getAttack(self, possible_attacks):
        pass

    # abstract
    def getHatch(self, possible_hatch):
        pass
