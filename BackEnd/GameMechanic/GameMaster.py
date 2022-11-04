from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameMechanic.Player import PlayerState
from BackEnd.GameObjects.Robal import Konik


class GameMaster(GameMechanic):
    def __init__(self):
        super().__init__()
        self.turn = 0
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
                print("Player " + self.winner_side)
                return

    def next_phase(self):
        if self.turn == 0:
            print("Tura białego atak.")
            self.BlackPlayer.set_state(PlayerState.INACTIVE)
            self.WhitePlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 1:
            print("Tura białego ruch.")
            self.WhitePlayer.set_state(PlayerState.MOVE)
        elif self.turn == 2:
            print("Tura białego wylęganie.")
            self.WhitePlayer.resources += self.getResourcesForSide("B")
            self.WhitePlayer.set_state(PlayerState.HATCH)
        elif self.turn == 3:
            print("Tura czarnego atak.")
            self.WhitePlayer.set_state(PlayerState.INACTIVE)
            self.BlackPlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 4:
            print("Tura czarnego ruch.")
            self.BlackPlayer.set_state(PlayerState.MOVE)
        elif self.turn == 5:
            print("Tura czarnego wylęganie.")
            self.BlackPlayer.resources += self.getResourcesForSide("C")
            self.BlackPlayer.set_state(PlayerState.HATCH)
            self.turn = -1
        self.turn += 1

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
