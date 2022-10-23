from Robal import *


class Armia:

    lastID = 0

    def getNewID(self):
        self.lastID = self.lastID + 1
        return self.lastID

    def __init__(self, newBug):
        self.ID = self.getNewID()
        self.numberOfMoves = 0
        self.bugList = [newBug]

    # def setNumberOfMoves(self):