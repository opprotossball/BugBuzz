from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameObjects.Robal import Konik


class GameMaster(GameMechanic):
    def __init__(self):
        super().__init__()
        self.turn = 0
        self.UI = None
        self.display = None

        self.winner_side = None

    def newGame(self, player_white, player_black):
        self.BlackPlayer = player_black
        self.WhitePlayer = player_white

        while True:
            self.nextMove()
            if self.gameIsOver():
                print("Player " + self.winner_side)
                return

    def nextMove(self):
        if self.turn == 0:
            print("Tura białego atak.")
            self.WhitePlayer.performAttack()
            self.updateWindow()
        elif self.turn == 1:
            print("Tura białego ruch.")
            self.WhitePlayer.performMove()
            self.updateWindow()
        elif self.turn == 2:
            print("Tura białego wylęganie.")
            self.WhitePlayer.resources += self.getResourcesForSide("B")
            self.WhitePlayer.performHatchery()
            self.updateWindow()
        elif self.turn == 3:
            print("Tura czarnego atak.")
            self.BlackPlayer.performAttack()
            self.updateWindow()
        elif self.turn == 4:
            print("Tura czarnego ruch.")
            self.BlackPlayer.performMove()
            self.updateWindow()
        elif self.turn == 5:
            print("Tura czarnego wylęganie.")
            self.BlackPlayer.resources += self.getResourcesForSide("C")
            self.BlackPlayer.performHatchery()
            self.turn = -1
            self.updateWindow()
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
