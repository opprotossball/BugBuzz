import math
import random

from BackEnd.GameObjects.Robal import *
from collections import Counter

from Util import Information


class Armia:
    def __init__(self):
        self.numberOfMoves = 0
        self.bugList = []
        self.numberOfGrassHoppers = 0
        self.attack = 0
        self.was_attacked = False

    def addBug(self, bug):
        if bug.short_name == "K":
            self.numberOfGrassHoppers += 1
        self.bugList.append(bug)
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
        return armyValidMoves


    def hasAttack(self):
        for bug in self.bugList:
            for neighbour in bug.field.getNeighbours():
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    return True
        return False

    def get_attacks(self):
        attackArray = []
        for bug in self.bugList:
            for neighbour in bug.field.getNeighbours():
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    if neighbour.bug.army in attackArray:
                        continue
                    else:
                        attackArray.append(neighbour.bug.army)
        return attackArray

    def isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(self, ourSide, neighbourField):
        return neighbourField is not None and neighbourField.bug is not None and neighbourField.bug.side is not ourSide

    def calculate_attack(self):
        attack_values = [0 for i in range(6)]
        for bug in self.bugList:
            attack_values[bug.attack] += 1
        for i in range(len(attack_values)-1, 0, -1):
            if attack_values[i] >= math.ceil(len(self.bugList) / 2):
                self.attack = i
                return i
            attack_values[i-1] += attack_values[i]
        self.attack = 0
        return 0

    def getToughnessArray(self):
        toughnessInterval = []
        for bug in self.bugList:
            newElement = bug.toughness
            if newElement in toughnessInterval:
                continue
            else:
                toughnessInterval += newElement
        return toughnessInterval

    def performMove(self, direction):
        for bug in self.bugList:
            bug.moved = False

        while not self.haveEveryBugMoved():
            for bug in self.bugList:
                bug.setMove(bug.move - 1)
                if not bug.moved:
                    dict = bug.field.getDictionary()
                    if bug.hasEnemyInSurrounding():
                        bug.moved = True
                    elif dict[direction] is not None:
                        if dict[direction].bug is None:
                            field = dict[direction]
                            bug.moveBugTo(field)
                            bug.moved = True
                        elif dict[direction].bug.moved:
                            bug.moved = True
                    else:
                        bug.moved = True
        self.numberOfMoves -= 1

    def haveEveryBugMoved(self):
        for bug in self.bugList:
            if not bug.moved:
                return False
        return True

    def has_bug_with_moves_to_examine(self):
        for bug in self.bugList:
            if len(bug.moveToExamine) > 0:
                return True
        return False

    def setMoves(self):
        moves = 20
        for bug in self.bugList:
            if moves > bug.move:
                moves = bug.move
        self.numberOfMoves = moves
