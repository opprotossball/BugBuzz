from BackEnd.Trader import Trader


def concatenate_moves(table1, table2):
    concatenated = []
    for el1 in table1:
        for el2 in table2:
            concatenated.append((el1, el2))
    return concatenated


class Interfejs:
    def __init__(self, GM, side):
        self.side = side
        self.resources = 0
        self.GameMaster = GM

    def performMove(self):
        choice = ""
        while choice != "end":
            armies = self.GameMaster.getArmies(self.side)
            moves = []
            for i in range(len(armies)):
                moves += self.create_moves([i], armies[i].getValidMoves)
            moves.append("end")
            move = self.getMove(moves)
            armies .performeMove(move)


    def performAttack(self):
        choice = ""
        while choice != "end":
            armies = self.GameMaster.getArmies(self.side)
            attacks = []
            for i in range(len(armies)):
                attacks += self.create_moves([i], armies[i].getAttacks())
            attacks.append("end")
            attack = self.getAttack(attacks)
            armies .performeMove(attack)

    def performHatchery(self):
        choice = ""
        while choice != "end" and self.GameMaster.isAvailableSpaceForHatch(self.side):
            trader = Trader()
            possible_to_hatch = trader.getOptions()
            hatchery_fields = []
            if self.side == "C":
                hatchery_fields = self.GameMaster.plansza.blacksHatchery
            elif self.side == "B":
                hatchery_fields = self.GameMaster.plansza.whitesHatchery
            for field in hatchery_fields:
                if field.bug is not None:
                    hatchery_fields.remove(field)

            possible_to_hatch = concatenate_moves(hatchery_fields, possible_to_hatch)
            possible_to_hatch.append("end")
            picked = self.getHatch(possible_to_hatch)
            if picked != "end":
                field, bug = picked
                trader.buyBug(bug, field)


    # abstract
    def getMove(self, possible_moves):
        pass

    # abstract
    def getAttack(self, possible_attacks):
        pass

    # abstract
    def getHatch(self, possible_hatch):
        pass
