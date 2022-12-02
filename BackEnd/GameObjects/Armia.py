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

    def get_toughness_array(self):
        toughnessInterval = []
        for bug in self.bugList:
            for newElement in bug.toughness:
                if newElement in toughnessInterval:
                    continue
                else:
                    toughnessInterval.append(newElement)
        return sorted(toughnessInterval)

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

    def setMoves(self):
        moves = 20
        for bug in self.bugList:
            if moves > bug.move:
                moves = bug.move
        self.numberOfMoves = moves
