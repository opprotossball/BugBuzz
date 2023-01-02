from BackEnd.GameObjects.Plansza import Plansza
from Util import Information


class Position:

    def __init__(self, board=None, turn=None, winner=None):
        self.winner_side = winner
        self.turn = turn
        self.board = board
        self.valid = False
        self.ready = False

    def set_starting_position(self):
        self.board = Plansza(Information.board_size)
        self.turn = 0
