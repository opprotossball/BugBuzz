import math

from RobaleProject.Util.HashMap import HashMap


class Position:
    def __init__(self, board):
        self.board = board
        self.evaluation = 0
        self.nextPositions = []


class Evaluator:
    def __init__(self, NN, side):
        self.NN = NN
        if side == "C":
            self.isMaximizing = False
        elif side == "B":
            self.isMaximizing = True
        self.position_root = None
        self.position_list = HashMap(1299457)

    def evaluate(self, position):
        self.position_root = Position(position)
        self.position_root.evaluation = self.minimax(position, 3, self.isMaximizing)
        return self.position_root.evaluation

    def evaluate_and_get_best_move(self, position):
        self.evaluate(position)


    def minimax(self, position, depth, maximazingP):
        if depth == 0:
            pos = self.get_position_from_list(position)

            if pos is None:
                pos = Position(position)
                pos.evaluation = self.NN.evaluate_at(position)
                self.add_position_to_list(pos)
            return pos

        if maximazingP:
            maxEval = - math.inf
            positions_and_probabilities = self.get_positions_from(position)
            for positions_priorities, probability in positions_and_probabilities:
                pos = Position(positions_priorities[0])
                pos_saved = self.get_position_from_list(pos)
                if pos_saved is None:
                    evaluation = 0
                    for position_with_priority in positions_priorities:
                        evaluation += probability * self.minimax(position_with_priority[0], depth - 1, False)
                    pos.evaluation = evaluation
                    position.nextPositions.append(pos)
                    maxEval = max(evaluation, maxEval)
                else:
                    evaluation = pos_saved.evaluation * probability
                    maxEval = max(evaluation, maxEval)
            return maxEval
        else:
            minEval = math.inf
            positions_and_probabilities = self.get_positions_from(position)
            for positions_priorities, probability in positions_and_probabilities:
                pos = Position(positions_priorities[0])
                pos_saved = self.get_position_from_list(pos)
                if pos_saved is None:
                    evaluation = 0
                    for position_with_priority in positions_priorities:
                        evaluation += position_with_priority[1] * self.minimax(position_with_priority[0], depth - 1, True)

                    pos.evaluation = evaluation
                    position.nextPositions.append(pos)

                    minEval = min(evaluation, minEval)
                else:
                    evaluation = pos_saved.evaluation * probability
                    minEval = min(evaluation, minEval)

            return minEval

    def get_positions_from(self, positions):
        positions_and_probabilities = []
        return positions_and_probabilities

    def get_position_from_list(self, position):
        hash = position.board.hash()
        return self.position_list.get(hash)

    def add_position_to_list(self, position):
        hash = position.board.hash()
        self.position_list.put(hash, position)

