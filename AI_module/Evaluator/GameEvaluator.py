import math

from AI_module.Evaluator.GameDictionary import GameDictionary
from BackEnd.GameMechanic.PositionGenerator import PositionGenerator
from Util.PlayerEnum import PlayerEnum


def s_w_k(value):
    return 1 - value[0].evalutionForBlack


def s_b_k(value):
    return 1 - value[0].evalutionForWhite


class EvaluatedPosition:
    def __init__(self, board):
        self.board = board

        self.evaluationForWhite = 0
        self.nextPositionsWhite = []  # (position_ref, board, moves, probability)

        self.evaluationForBlack = 0
        self.nextPositionsBlack = []

    def sort_for_white(self):
        self.nextPositionsWhite.sort(key=s_w_k)

    def sort_for_black(self):
        self.nextPositionsBlack.sort(key=s_b_k)


class Evaluator:
    def __init__(self, NN):
        self.NN = NN

        self.position_root = None
        self.position_list = GameDictionary()

        self.generator = PositionGenerator()

        self.number_of_simulation = 0

    def evaluate(self, position, player, depth=3):
        if player == PlayerEnum.B:
            isMaximizing = True
        else:
            isMaximizing = False
        self.position_root = EvaluatedPosition(position)
        self.position_root.evaluation = self.minimax(position, depth, isMaximizing)
        return self.position_root.evaluation

    def get_moves(self, positions, player):
        pos = self.position_list.get_position_from_list(positions)
        if player == PlayerEnum.B:
            pos.sort_for_white()
            return pos.nextPositionsWhite[2], pos.nextPositionsWhite[1]
        else:
            pos.sort_for_black()
            return pos.nextPositionsBlack[2], pos.nextPositionsBlack[1]

    def minimax(self, position, depth, maximazingP):
        if depth == 0:
            pos = self.get_position_from_list(position)

            if pos is None:
                pos = EvaluatedPosition(position)
                pos.evaluation = self.NN.evaluate_at(position)
                self.add_position_to_list(pos)
            return pos

        if maximazingP:
            maxEval = - math.inf
            positions_and_probabilities = self.get_positions_from(position)
            for positions_priorities, probability in positions_and_probabilities:
                pos = EvaluatedPosition(positions_priorities[0])
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
            self.number_of_simulation += 1
            return maxEval
        else:
            minEval = math.inf
            positions_and_probabilities = self.get_positions_from(position)
            for positions_priorities, probability in positions_and_probabilities:
                pos = EvaluatedPosition(positions_priorities[0])
                pos_saved = self.get_position_from_list(pos)
                if pos_saved is None:
                    evaluation = 0
                    for position_with_priority in positions_priorities:
                        evaluation += position_with_priority[1] * self.minimax(position_with_priority[0], depth - 1,
                                                                               True)

                    pos.evaluation = evaluation
                    position.nextPositions.append(pos)

                    minEval = min(evaluation, minEval)
                else:
                    evaluation = pos_saved.evaluation * probability
                    minEval = min(evaluation, minEval)

            self.number_of_simulation += 1
            return minEval

    def get_positions_from(self, position):
        positions_and_probabilities = self.generator.getPosititions(position)
        return positions_and_probabilities

    def get_position_from_list(self, position):
        return self.position_list.get_position_from_list(position)

    def add_position_to_list(self, position):
        self.position_list.add_position_to_list(position, True)
