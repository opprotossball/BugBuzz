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
            self.bugList.append(self, pole.bug)
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

    def performMove(self, direction):
        for bug in self.bugList:
            if direction == 'WN':
                bug.setField(bug.filed.WN)
            elif direction == 'EN':
                bug.setField(bug.filed.EN)
            elif direction == 'E':
                bug.setField(bug.filed.E)
            elif direction == 'ES':
                bug.setField(bug.filed.ES)
            elif direction == 'WS':
                bug.setField(bug.filed.WS)
            elif direction == 'W':
                bug.setField(bug.filed.W)
            else:
                print('Cannot change direction')
                return
        self.numberOfMoves = self.numberOfMoves-1

    def getValidMoves(self):
        validMoves = ['WN', 'EN', 'E', 'ES', 'WS', 'W']

        for bugg in self.bugList:
            if bugg.field.WN is not None:
                if bugg.field.WN.bug is not None and (bugg.field.WN.bug.side is not bugg.side):
                    validMoves.remove(self, 'WN')
            elif bugg.field.WN is None:
                validMoves.remove(self, 'WN')

            if bugg.field.EN is not None:
                if bugg.field.EN.bug is not None and (bugg.field.EN.bug.side is not bugg.side):
                    validMoves.remove(self, 'EN')
            elif bugg.field.EN is None:
                validMoves.remove(self, 'EN')

            if bugg.field.E is not None:
                if bugg.field.E.bug is not None and (bugg.field.E.bug.side is not bugg.side):
                    validMoves.remove(self, 'E')
            elif bugg.field.E is None:
                validMoves.remove(self, 'E')

            if bugg.field.ES is not None:
                if bugg.field.ES.bug is not None and (bugg.field.ES.bug.side is not bugg.side):
                    validMoves.remove(self, 'ES')
            elif bugg.field.ES is None:
                validMoves.remove(self, 'ES')

            if bugg.field.WS is not None:
                if bugg.field.WS.bug is not None and (bugg.field.WS.bug.side is not bugg.side):
                    validMoves.remove(self, 'WS')
            elif bugg.field.WS is None:
                validMoves.remove(self, 'WS')

            if bugg.field.W is not None:
                if bugg.field.W.bug is not None and (bugg.field.W.bug.side is not bugg.side):
                    validMoves.remove(self, 'W')
            elif bugg.field.W is None:
                validMoves.remove(self, 'W')

        return validMoves

    def hasAttack(self):
        for bugg in self.bugList:
            if bugg.field.WN is not None:
                if bugg.field.WN.bug is not None and (bugg.field.WN.bug.side is not bugg.side):
                    return True

            if bugg.field.EN is not None:
                if bugg.field.EN.bug is not None and (bugg.field.EN.bug.side is not bugg.side):
                    return True

            if bugg.field.E is not None:
                if bugg.field.E.bug is not None and (bugg.field.E.bug.side is not bugg.side):
                    return True

            if bugg.field.ES is not None:
                if bugg.field.ES.bug is not None and (bugg.field.ES.bug.side is not bugg.side):
                    return True

            if bugg.field.WS is not None:
                if bugg.field.WS.bug is not None and (bugg.field.WS.bug.side is not bugg.side):
                    return True

            if bugg.field.W is not None:
                if bugg.field.W.bug is not None and (bugg.field.W.bug.side is not bugg.side):
                    return True

        return False

    def getNumberOfResources(self):

        grassHopperCounter = 0
        hatcheryCounter = 0;
        for bugg in self.bugList:
            if type(bugg) == Konik:
                grassHopperCounter = grassHopperCounter + 1
            if bugg.field.hatchery == True:
                hatcheryCounter = hatcheryCounter + 1

        return grassHopperCounter*hatcheryCounter
