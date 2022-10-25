import random

from BackEnd.Robal import *
from collections import Counter

from Util import Information


class Armia:
    def __init__(self, pole):
        self.numberOfMoves = 0
        self.bugList = []
        if pole.bug is not None:
            self.bugList.append(pole.bug)
            pole.bug.army = self

    def addRobal(self, bug):
        self.bugList.append(bug)
        bug.army = self

    def performMove(self, direction):
        for bug in self.bugList:
            if bug.move != 0:
                if direction not in Information.directionOptions:
                    print('Cannot change direction')
                    return
                field = bug.field.direction(direction)
                bug.setField(field)
                bug.move -= 1

    def getValidMoves(self):
        validMoves = ['WN', 'EN', 'E', 'ES', 'WS', 'W']

        for bug in self.bugList:
            for neighbour, name_of_direction in zip(bug.field.neighbours, bug.field.directions):
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    validMoves.remove(name_of_direction)
                elif neighbour is None:
                    validMoves.remove(name_of_direction)

        return validMoves

    def hasAttack(self):
        for bug in self.bugList:
            for neighbour in bug.field.neighbours:
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    return True
        return False

    def getAttacks(self):
        attackArray = []
        for bug in self.bugList:
            for neighbour in bug.field.neighbours:
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    if neighbour.bug.army in attackArray:
                        continue
                    else:
                        attackArray.append(neighbour.bug.army)
        return attackArray

    def isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(self, ourSide, neighbourField):
        return neighbourField is not None and neighbourField.bug is not None and neighbourField.bug.side is not ourSide

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

    def performAttack(self, opponentArmy):
        myArmies = []
        myWarriors = []
        attackers = []
        diceCounter = 0

        for bug in opponentArmy.bugList:
            for neighbour in bug.field.neighbours:
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    if bug in attackers:
                        continue
                    else:
                        attackers.append(bug)

                    if neighbour.bug in myWarriors:
                        continue
                    else:
                        myWarriors.append(neighbour.bug)

                    if neighbour.bug.army in myArmies:
                        continue
                    else:
                        myArmies.append(neighbour.bug.army)

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
