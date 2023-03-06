from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameMechanic.Player import PlayerState
from BackEnd.GameObjects.Plansza import Plansza
from Util import Information
from Util.PlayerEnum import PlayerEnum


class GameMaster(GameMechanic):
    def __init__(self):
        super().__init__()
        self.turn = -1
        self.playing_online = False
        self.ui = None
        self.display = None
        self.winner_side = None
        self.active = None

    def update_window(self):
        if self.display is not None:
            self.display.update_window()

    def new_game(self, player_white, player_black, board=None, start_at_turn=None, ui=True):
        self.winner_side = None

        if board is not None:
            self.set_board(board)
        else:
            self.set_board(Plansza(Information.board_size))

        if start_at_turn is not None:
            self.turn = start_at_turn
        else:
            self.turn = -1

        self.set_player(player_white)
        self.set_player(player_black)
        if ui:
            self.set_new_ui()
        self.next_phase()

    def next_phase(self):
        self.get_armies(PlayerEnum.B)
        self.get_armies(PlayerEnum.C)
        self.turn += 1
        if self.turn == 6:
            self.turn = 0
        if self.turn == 0:
            self.BlackPlayer.set_state(PlayerState.INACTIVE)
            self.WhitePlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 1:
            self.WhitePlayer.set_state(PlayerState.MOVE)
        elif self.turn == 2:
            self.reset_move(PlayerEnum.B)
            self.WhitePlayer.resources = self.get_resources_for_side(PlayerEnum.B)
            self.WhitePlayer.set_state(PlayerState.HATCH)
        elif self.turn == 3:
            self.WhitePlayer.set_state(PlayerState.INACTIVE)
            self.BlackPlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 4:
            self.BlackPlayer.set_state(PlayerState.MOVE)
        elif self.turn == 5:
            self.reset_move(PlayerEnum.C)
            self.BlackPlayer.resources = self.get_resources_for_side(PlayerEnum.C)
            self.BlackPlayer.set_state(PlayerState.HATCH)

    def set_phase(self, turn):
        self.turn = turn - 1
        self.next_phase()

    def game_is_over(self):
        bug = self.board.resources[0].bug
        if bug is not None:
            side = bug.side
        else:
            return False

        for pole in self.board.resources:
            if pole.bug is None or pole.bug.side != side:
                return False

        self.winner_side = side
        return True

    def get_active_player(self):
        if self.WhitePlayer.state != PlayerState.INACTIVE:
            return PlayerEnum.B
        elif self.BlackPlayer.state != PlayerState.INACTIVE:
            return PlayerEnum.C
