import random

from Robal import *
from Pole import *
from collections import Counter


class Armia:

    lastID = 0

    def getNewID(self):
        self.lastID = self.lastID + 1
        return self.lastID

    def __init__(self, pole):
        self.ID = self.getNewID()
        self.numberOfMoves = 0
        self.bugList = []
        if pole.bug is not None:
            self.bugList.append(pole.bug)
            pole.bug.armyID = self.ID

    def performMove(self, direction):
        for bug in self.bugList:
            if bug.move != 0:
                if direction == 'WN':
                    bug.setField(bug.field.WN)
                elif direction == 'EN':
                    bug.setField(bug.field.EN)
                elif direction == 'E':
                    bug.setField(bug.field.E)
                elif direction == 'ES':
                    bug.setField(bug.field.ES)
                elif direction == 'WS':
                    bug.setField(bug.field.WS)
                elif direction == 'W':
                    bug.setField(bug.field.W)
                else:
                    print('Cannot change direction')
                    return
                bug.move -= 1

    def getValidMoves(self):
        validMoves = ['WN', 'EN', 'E', 'ES', 'WS', 'W']

        for bugg in self.bugList:
            if bugg.field.WN is not None:
                if bugg.field.WN.bug is not None and (bugg.field.WN.bug.side is not bugg.side):
                    validMoves.remove('WN')
            elif bugg.field.WN is None:
                validMoves.remove('WN')

            if bugg.field.EN is not None:
                if bugg.field.EN.bug is not None and (bugg.field.EN.bug.side is not bugg.side):
                    validMoves.remove('EN')
            elif bugg.field.EN is None:
                validMoves.remove('EN')

            if bugg.field.E is not None:
                if bugg.field.E.bug is not None and (bugg.field.E.bug.side is not bugg.side):
                    validMoves.remove('E')
            elif bugg.field.E is None:
                validMoves.remove('E')

            if bugg.field.ES is not None:
                if bugg.field.ES.bug is not None and (bugg.field.ES.bug.side is not bugg.side):
                    validMoves.remove('ES')
            elif bugg.field.ES is None:
                validMoves.remove('ES')

            if bugg.field.WS is not None:
                if bugg.field.WS.bug is not None and (bugg.field.WS.bug.side is not bugg.side):
                    validMoves.remove('WS')
            elif bugg.field.WS is None:
                validMoves.remove('WS')

            if bugg.field.W is not None:
                if bugg.field.W.bug is not None and (bugg.field.W.bug.side is not bugg.side):
                    validMoves.remove('W')
            elif bugg.field.W is None:
                validMoves.remove('W')

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

    def getAttacks(self):

        attackArray = []
        for bugg in self.bugList:
            if bugg.field.WN is not None:
                if bugg.field.WN.bug is not None and (bugg.field.WN.bug.side is not bugg.side):
                    if bugg.field.WN.bug.armyID in attackArray:
                        continue
                    else:
                        attackArray.append(bugg.field.WN.bug.armyID)

            if bugg.field.EN is not None:
                if bugg.field.EN.bug is not None and (bugg.field.EN.bug.side is not bugg.side):
                    if bugg.field.EN.bug.armyID in attackArray:
                        continue
                    else:
                        attackArray.append(bugg.field.EN.bug.armyID)

            if bugg.field.E is not None:
                if bugg.field.E.bug is not None and (bugg.field.E.bug.side is not bugg.side):
                    if bugg.field.E.bug.armyID in attackArray:
                        continue
                    else:
                        attackArray.append(bugg.field.E.bug.armyID)

            if bugg.field.ES is not None:
                if bugg.field.ES.bug is not None and (bugg.field.ES.bug.side is not bugg.side):
                    if bugg.field.ES.bug.armyID in attackArray:
                        continue
                    else:
                        attackArray.append(bugg.field.ES.bug.armyID)

            if bugg.field.WS is not None:
                if bugg.field.WS.bug is not None and (bugg.field.WS.bug.side is not bugg.side):
                    if bugg.field.WS.bug.armyID in attackArray:
                        continue
                    else:
                        attackArray.append(bugg.field.WS.bug.armyID)

            if bugg.field.W is not None:
                if bugg.field.W.bug is not None and (bugg.field.W.bug.side is not bugg.side):
                    if bugg.field.W.bug.armyID in attackArray:
                        continue
                    else:
                        attackArray.append(bugg.field.W.bug.armyID)

        return attackArray

    def getAttackPower(self, army):
        attackValue = Counter(army.bugList.attack)
        sorted(attackValue, key=attackValue.keys(), reverse=True)

        bugCount = 0
        for count, value in attackValue.items():
            bugCount += count
            if bugCount > attackValue.total()*0.5:
                finalValue = value
                break

        return finalValue

    def rollDice(self, diceCount):
        rollArray = []*diceCount
        i = 0
        while i < diceCount:
            rollArray[i] = random.randint(1, 10)
            i += 1

        return rollArray

    def getToughnessArray(self, attackers):

        toughnessInterval = []
        for i in attackers:
            newElement = attackers[i].toughness
            if newElement in toughnessInterval:
                continue
            else:
                toughnessInterval += newElement

        return toughnessInterval

    def performAttack(self, opponentArmyID):

        myArmies = []
        myWarriors = []
        attackers = []
        diceCounter = 0

        for bugg in opponentArmyID.bugList:
            if bugg.field.WN is not None:
                if bugg.field.WN.bug is not None and (bugg.field.WN.bug.side is not bugg.side):
                    if bugg in attackers:
                        continue
                    else:
                        attackers.append(bugg)

                    if bugg.field.WN.bug in myWarriors:
                        continue
                    else:
                        myWarriors.append(bugg.field.WN.bug)

                    if bugg.field.WN.bug.armyID in myArmies:
                        continue
                    else:
                        myArmies.append(bugg.field.WN.bug.armyID)

            if bugg.field.EN is not None:
                if bugg.field.EN.bug is not None and (bugg.field.EN.bug.side is not bugg.side):
                    if bugg in attackers:
                        continue
                    else:
                        attackers.append(bugg)

                    if bugg.field.EN.bug in myWarriors:
                        continue
                    else:
                        myWarriors.append(bugg.field.EN.bug)

                    if bugg.field.EN.bug.armyID in myArmies:
                        continue
                    else:
                        myArmies.append(bugg.field.EN.bug.armyID)

            if bugg.field.E is not None:
                if bugg.field.E.bug is not None and (bugg.field.E.bug.side is not bugg.side):
                    if bugg in attackers:
                        continue
                    else:
                        attackers.append(bugg)

                    if bugg.field.E.bug in myWarriors:
                        continue
                    else:
                        myWarriors.append(bugg.field.E.bug)

                    if bugg.field.E.bug.armyID in myArmies:
                        continue
                    else:
                        myArmies.append(bugg.field.E.bug.armyID)

            if bugg.field.ES is not None:
                if bugg.field.ES.bug is not None and (bugg.field.ES.bug.side is not bugg.side):
                    if bugg in attackers:
                        continue
                    else:
                        attackers.append(bugg)

                    if bugg.field.ES.bug in myWarriors:
                        continue
                    else:
                        myWarriors.append(bugg.field.ES.bug)

                    if bugg.field.ES.bug.armyID in myArmies:
                        continue
                    else:
                        myArmies.append(bugg.field.ES.bug.armyID)

            if bugg.field.WS is not None:
                if bugg.field.WS.bug is not None and (bugg.field.WS.bug.side is not bugg.side):
                    if bugg in attackers:
                        continue
                    else:
                        attackers.append(bugg)

                    if bugg.field.WS.bug in myWarriors:
                        continue
                    else:
                        myWarriors.append(bugg.field.WS.bug)

                    if bugg.field.WS.bug.armyID in myArmies:
                        continue
                    else:
                        myArmies.append(bugg.field.WS.bug.armyID)

            if bugg.field.W is not None:
                if bugg.field.W.bug is not None and (bugg.field.W.bug.side is not bugg.side):
                    if bugg in attackers:
                        continue
                    else:
                        attackers.append(bugg)

                    if bugg.field.W.bug in myWarriors:
                        continue
                    else:
                        myWarriors.append(bugg.field.W.bug)

                    if bugg.field.W.bug.armyID in myArmies:
                        continue
                    else:
                        myArmies.append(bugg.field.W.bug.armyID)

        for army in myArmies:
            diceCounter = diceCounter + self.getAttackPower(army)

        diceCounter = diceCounter + myWarriors.__len__()
        rollOutcomes = self.rollDice(diceCounter)
        opponentArmyToughness = self.getToughnessArray(attackers)

        hitNumber = 0
        for x in rollOutcomes:
            if x not in opponentArmyToughness:
                hitNumber += 1

        return hitNumber

    def getNumberOfResources(self):

        grassHopperCounter = 0
        hatcheryCounter = 0
        for bugg in self.bugList:
            if type(bugg) == Konik:
                grassHopperCounter = grassHopperCounter + 1
            if bugg.field.hatchery:
                hatcheryCounter = hatcheryCounter + 1

        return grassHopperCounter*hatcheryCounter
