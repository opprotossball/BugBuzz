from BackEnd.GameMechanic.Player import Player, PlayerState
from BackEnd.GameObjects.Trader import Trader


def concatenate_moves(table1, table2):
    concatenated = []
    for el1 in table1:
        for el2 in table2:
            concatenated.append((el1, el2))
    return concatenated


class NNPlayer(Player):

    def __init__(self, gm, side, evaluator):
        super().__init__(gm, side)
        self.evaluator = evaluator
        self.moves = None

    def set_state(self, state):  # ważne
        self.state = state
        if state == PlayerState.COMBAT:
            self.end_phase()
            pass  # to i tak tzreba jeszcze ogarnąć
        elif state == PlayerState.MOVE:
            self.perform_moves()
            self.end_phase()
        elif state == PlayerState.HATCH:
            self.perform_hatchery()
            self.end_phase()

    def oppositeSide(self):
        if self.side == "B":
            return "C"
        else:
            return "B"

    def perform_attacks(self):
        choice = ""
        while choice != "end":
            armies = self.gm.get_armies(self.oppositeSide())
            attacks = []
            for armies_index in range(len(armies)):
                if self.gm.ui is None:
                    attacks += concatenate_moves([armies_index], armies[armies_index].get_attacks())
                else:
                    attacks += armies
                    break
            attacks.append("end")
            if len(attacks) > 1:
                choice = self.get_attack(attacks)
            else:
                choice = "end"
            if choice != "end":
                index, attacked_army = choice
                self.perform_attack(attacked_army)
                #armies[index].performeMove(attacked_army)

    def perform_moves(self):
        choice = ""
        while choice != "end":
            armies = self.gm.get_armies(self.side)
            moves = []
            for index_army in range(len(armies)):
                if armies[index_army].numberOfMoves == 0:
                    continue
                moves += concatenate_moves([index_army], armies[index_army].getValidMoves())

            moves.append("end")
            if len(moves) > 1:
                choice = self.get_move(moves)
            else:
                choice = "end"
            if choice != "end":
                army_index, direction = choice
                self.perform_move(armies[army_index], direction)

    def perform_hatchery(self):
        choice = ""
        while choice != "end" and self.gm.isAvailableSpaceForHatch(self.side):
            trader = Trader()
            possible_to_hatch = trader.getOptions(self.resources)
            hatchery_fields = []
            if self.side == "C":
                hatchery_fields = self.gm.board.blacksHatchery
            elif self.side == "B":
                hatchery_fields = self.gm.board.whitesHatchery

            options = []

            for i in range(len(hatchery_fields)):
                if hatchery_fields[i].bug is None:
                    if self.gm.ui is None:
                        options.append(i)
                    else:
                        options.append(hatchery_fields[i])

            possible_to_hatch = concatenate_moves(options, possible_to_hatch)
            possible_to_hatch.append("end")
            choice = self.get_hatch(possible_to_hatch)
            if choice != "end":
                field, bug = choice
                self.perform_hatch(bug, field)

    def get_attack(self, possible_attacks):
        attack = self.attack_game[self.attack_counter]
        self.move_counter += 1
        if attack not in possible_attacks:
            print("Invalid move:" + attack + " not in " + possible_attacks)
            return None
        else:
            return attack

    def get_move(self, possible_moves):
        self.reset_move()
        move = self.moves_game[self.move_counter]
        self.move_counter += 1
        if move not in possible_moves:
            print("Invalid move:" + move + " not in " + possible_moves)
            return None
        else:
            return move

    def get_hatch(self, possible_hatch):
        hatch = self.hatch_game[self.hatch_game]
        self.move_counter += 1
        if hatch not in possible_hatch:
            print("Invalid move:" + hatch + " not in " + possible_hatch)
            return None
        else:
            return hatch

    def reset_move(self):
        position = self.gm.board.clone()
        self.moves = self.evaluator.evaluate_and_get_best_move(position)
        self.moves_game = self.moves[0]
        self.move_counter = 0
        self.attack_game = self.moves[1]
        self.attack_counter = 0
        self.hatch_game = self.moves[2]
        self.hatch_counter = 0
