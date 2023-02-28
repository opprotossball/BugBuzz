from BackEnd.GameObjects.Plansza import Plansza
from Util import Information


class Position:

    def __init__(self, board=None, turn=None, winner=None):
        self.winner_side = winner
        self.turn = turn
        self.board = board
        self.valid = False
        self.ready = False
        self.highlighted_by_active = []
        self.attacked_by_active = None
        self.active_leader = None
        self.active_rolls = []
        self.active_kills = 0

    def set_starting_position(self):
        self.board = Plansza(Information.board_size)
        self.turn = 0
