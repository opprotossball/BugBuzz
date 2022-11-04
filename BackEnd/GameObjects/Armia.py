import math
import random

from BackEnd.GameObjects.Robal import *
from collections import Counter

from Util import Information


class Armia:
    def __init__(self):
        self.numberOfMoves = 20
        self.bugList = []
        self.numberOfGrassHoppers = 0

    def addBug(self, bug):
        if bug.short_name == "K":
            self.numberOfGrassHoppers += 1
        self.bugList.append(bug)
        self.numberOfMoves = min(self.numberOfMoves, bug.move_left)
        bug.army = self

    def getValidMoves(self):
        for bug in self.bugList:
            bug.moveToExamine = Information.directionOptions.copy()
            bug.validMoves = []
            bug.invalidMoves = []

        while self.has_bug_with_moves_to_examine():
            for bug in self.bugList:
                move_to_examine = bug.moveToExamine.copy()
                for name_of_direction in bug.moveToExamine:
                    neighbour = bug.field.getDictionary()[name_of_direction]
                    if neighbour is None:  # Pole nie istnieje
                        move_to_examine.remove(name_of_direction)
                        bug.invalidMoves.append(name_of_direction)
                    elif neighbour.bug is not None:  # Pole istnieje i znajduje się na nim robal
                        if neighbour.bug.side != bug.side:  # Przeciwnika
                            bug.moveToExamine = []
                            bug.validMoves = []
                            bug.invalidMoves = Information.directionOptions.copy()
                            break
                        elif name_of_direction in neighbour.bug.validMoves:  # Nasz i może on się ruszyć w kierunku
                            move_to_examine.remove(name_of_direction)
                            bug.validMoves.append(name_of_direction)
                        elif name_of_direction in neighbour.bug.invalidMoves:  # Nasz i nie może on się ruszyć w kierunku
                            move_to_examine.remove(name_of_direction)
                            bug.invalidMoves.append(name_of_direction)
                    else:  # Na polu nic nie ma
                        move_to_examine.remove(name_of_direction)
                        bug.validMoves.append(name_of_direction)
                    bug.moveToExamine = move_to_examine

        armyValidMoves = []
        for bug in self.bugList:
            for move in bug.validMoves:
                if move not in armyValidMoves:
                    armyValidMoves.append(move)
                if armyValidMoves == Information.directionOptions:
                    return armyValidMoves
            bug.move_left -= 1
        return armyValidMoves

    def performMove(self, direction):
        for bug in self.bugList:
            bug.state = "to move"

        while not self.haveEveryBugMoved():
            for bug in self.bugList:
                if bug.state == "to move":
                    dict = bug.field.getDictionary()
                    if bug.hasEnemyInSurrounding():
                        bug.state = "won't move"
                    elif dict[direction] is not None:
                        if dict[direction].bug is None:
                            field = dict[direction]
                            bug.moveBugTo(field)
                            bug.state = "moved"
                        elif dict[direction].bug.state == "won't move":
                            bug.state = "won't move"
                    else:
                        bug.state = "won't move"
        self.numberOfMoves -= 1
        for bug in self.bugList:
            bug.move_left -= 1

    def setMove(self):
        self.numberOfMoves = 20
        for bug in self.bugList:
            bug.move_left = bug.move
            self.numberOfMoves = min(self.numberOfMoves, bug.move)

    def performAttack(self, opponentArmy):
        myArmies = []
        myWarriors = []
        attackers = []
        diceCounter = 0

        for bug in opponentArmy.bugList:
            for neighbour in bug.field.getNeighbours():
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


    def hasAttack(self):
        for bug in self.bugList:
            for neighbour in bug.field.getNeighbours():
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    return True
        return False

    def getAttacks(self):
        attackArray = []
        for bug in self.bugList:
            for neighbour in bug.field.getNeighbours():
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    if neighbour.bug.army in attackArray:
                        continue
                    else:
                        attackArray.append(neighbour.bug.army)
        return attackArray

    def getAttackPower(self, army):
        attackValue = Counter(army.bugList.attack)
        sorted(attackValue, key=attackValue.keys(), reverse=True)
        index = math.ceil((attackValue + 1)/2)
        return attackValue[index]

    def getToughnessArray(self, attackers):

        toughnessInterval = []
        for i in attackers:
            newElement = attackers[i].toughness
            if newElement in toughnessInterval:
                continue
            else:
                toughnessInterval += newElement

        return toughnessInterval

    def isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(self, ourSide, neighbourField):
        return neighbourField is not None and neighbourField.bug is not None and neighbourField.bug.side is not ourSide

    def rollDice(self, diceCount):
        rollArray = [] * diceCount
        i = 0
        while i < diceCount:
            rollArray[i] = random.randint(1, 10)
            i += 1

        return rollArray

    def haveEveryBugMoved(self):
        for bug in self.bugList:
            if bug.state == "to move":
                return False
        return True

    def getNumberOfResources(self):
        grassHopperCounter = 0
        hatcheryCounter = 0
        for bug in self.bugList:
            if type(bug) == Konik:
                grassHopperCounter = grassHopperCounter + 1
            if bug.field.hatchery:
                hatcheryCounter = hatcheryCounter + 1

        return grassHopperCounter * hatcheryCounter

    def has_bug_with_moves_to_examine(self):
        for bug in self.bugList:
            if len(bug.moveToExamine) > 0:
                return True
        return False
