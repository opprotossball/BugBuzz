from BackEnd.GameObjects.Robal import *


class Armia:
    def __init__(self, board):
        self.numberOfMoves = 0
        self.bugList = []
        self.numberOfGrassHoppers = 0
        self.attack = 0
        self.was_attacked = False
        self.board = board

    def addBug(self, bug):
        if bug.short_name == RobalEnum.K:
            self.numberOfGrassHoppers += 1
        self.bugList.append(bug)
        bug.army = self
