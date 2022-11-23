from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameMechanic.Player import PlayerState
from BackEnd.GameObjects.Robal import Konik


class GameMaster(GameMechanic):
    def __init__(self):
        super().__init__()
        self.turn = -1
        self.ui = None
        self.display = None

        self.winner_side = None

    def newGame(self, player_white, player_black):
        self.BlackPlayer = player_black
        self.WhitePlayer = player_white
        self.next_phase()

        while True:
            self.updateWindow()
            if self.gameIsOver():
                print("Player " + self.winner_side + " has won!")
                return

    def next_phase(self):
        self.turn += 1
        if self.turn == 6:
            self.turn = 0
        if self.turn == 0:
            self.BlackPlayer.set_state(PlayerState.INACTIVE)
            self.WhitePlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 1:
            self.getArmies("C")
            self.resetMove("B")
            self.WhitePlayer.set_state(PlayerState.MOVE)
        elif self.turn == 2:
            self.WhitePlayer.resources = self.getResourcesForSide("B")
            self.WhitePlayer.set_state(PlayerState.HATCH)
        elif self.turn == 3:
            self.WhitePlayer.set_state(PlayerState.INACTIVE)
            self.BlackPlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 4:
            self.getArmies("B")
            self.resetMove("C")
            self.BlackPlayer.set_state(PlayerState.MOVE)
        elif self.turn == 5:
            self.BlackPlayer.resources = self.getResourcesForSide("C")
            self.BlackPlayer.set_state(PlayerState.HATCH)

    def gameIsOver(self):
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
