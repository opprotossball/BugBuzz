from AI_module.AI.TerminalStatesTracker import TerminalStatesTracker
from BackEnd.GameMechanic.GameMaster import GameMaster
from Util.Stack import Stack

class Brain:
    def __init__(self, evaluator, tst, max_simulation=1024):
        self.evaluator = evaluator
        self.max_simulation = max_simulation
        self.game = Stack()
        self.TST = tst

    def get_attack(self, board):
        pass

    def get_move(self, board):
        pass

    def get_hatch(self):
        pass

    def simulate_game(self, position, player_to_move):
        game = GameMaster()
        self.game.put((position, 0))

        for simulation in range(self.max_simulation):
            position, priority = self.game.pop()

            if game.gameIsOver(position):
                self.TST.add_state(position, game.winner_side)
                if self.game.isEmpty():
                    self.game.put((self.evaluator.get_random_postion(), 0))  # TODO
                position, priority = self.game.pop()

            attack, moves, hatches, boards = self.evaluator.get_moves(position)

            game.performAttack(player_to_move, attack)
            for i, board in enumerate(boards):
                if game.board == board:
                    game.performMove(moves[i][0], moves[i][1])
                    game.performAttack(attack[i][0], attack[i][0])
                    break

            self.game.put((position, priority + 1))
            position = game.board
            self.game.put(position)
