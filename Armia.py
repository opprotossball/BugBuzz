from Robal import *
from Pole import *
from collections import Counter

class Armia:

    lastID = 0

    def getNewID(self):
        self.lastID = self.lastID + 1
        return self.lastID

    def __init__(self, pole ):
        self.ID = self.getNewID()
        self.numberOfMoves = 0
        self.bugList = []
        if pole.bug is not None:
            self.bugList.add(self, pole.bug)
            pole.bug.armyID = self.ID

    def setNumberOfMoves(self):
        bugMoves = Counter(self.bugList.move)
        sorted(bugMoves, key=bugMoves.keys(), reverse=True)

        bugCount = 0
        for count, value in bugMoves.items():
            bugCount += count
            if bugCount > bugMoves.total()*0.5:
                moveValue = value
                break

        self.numberOfMoves = moveValue
