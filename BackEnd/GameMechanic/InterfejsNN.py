from BackEnd.GameMechanic.Interfejs import Interfejs


class InterfejNN(Interfejs):
    def __init__(self, evaluator, GM, side, updateMethod):
        super().__init__(GM, side, updateMethod)
        self.side = side
        self.evaluator = evaluator
        self.moves = None # ([ruchy armii], [ataki armii(lista priorytetu ataku)], [wylęganie])

    def resetMove(self):
        position = self.GM.board.clone()
        self.moves = self.evaluator.evaluate_and_get_best_move(position)
        self.moves_game = self.moves[0]
        self.move_counter = 0
        self.attack_game = self.moves[1]
        self.attack_counter = 0
        self.hatch_game = self.moves[2]
        self.hatch_counter = 0

    def getMove(self, possible_moves):
        self.resetMove()
        move = self.moves_game[self.move_counter]
        self.move_counter += 1
        if move not in possible_moves:
            print("Invalid move:" + move + " not in " + possible_moves)
            return None
        else:
            self.GM.updateWindow()
            return move

    def getAttack(self, possible_attacks):
        attack = self.attack_game[self.attack_counter]
        self.move_counter += 1
        if attack not in possible_attacks:
            print("Invalid move:" + attack + " not in " + possible_attacks)
            return None
        else:
            self.GM.updateWindow()
            return attack

    def getHatch(self, possible_hatch):
        hatch = self.hatch_game[self.hatch_game]
        self.move_counter += 1
        if hatch not in possible_hatch:
            print("Invalid move:" + hatch + " not in " + possible_hatch)
            return None
        else:
            self.GM.updateWindow()
            return hatch
