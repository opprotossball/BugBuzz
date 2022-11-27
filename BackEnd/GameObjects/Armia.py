import math
from queue import PriorityQueue

from BackEnd.GameObjects.Robal import *
from Util import Information


class Armia:
    def __init__(self):
        self.numberOfMoves = 0
        self.bugList = []
        self.numberOfGrassHoppers = 0
        self.attack = 0
        self.was_attacked = False

    def addBug(self, bug):
        if bug.short_name == RobalEnum.K:
            self.numberOfGrassHoppers += 1
        self.bugList.append(bug)
        bug.army = self

    def getValidMoves(self):
        for bug in self.bugList:
            bug.moveToExamine = Information.directionOptions.copy()
            bug.validMoves = []
            bug.invalidMoves = []

        queue = PriorityQueue()

        for bug in self.bugList:
            queue.put((6, bug))

        while not queue.empty():
            priority, bug = queue.get()
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
                        priority = 0
                        break
                    elif name_of_direction in neighbour.bug.validMoves:  # Nasz i może on się ruszyć w kierunku
                        move_to_examine.remove(name_of_direction)
                        bug.validMoves.append(name_of_direction)
                        priority -= 1
                    elif name_of_direction in neighbour.bug.invalidMoves:  # Nasz i nie może on się ruszyć w kierunku
                        move_to_examine.remove(name_of_direction)
                        bug.invalidMoves.append(name_of_direction)
                        priority -= 1

                else:  # Na polu nic nie ma
                    move_to_examine.remove(name_of_direction)
                    bug.validMoves.append(name_of_direction)
                    priority -= 1
                bug.moveToExamine = move_to_examine
            if priority > 0:
                queue.put((priority, bug))

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
        for i in range(len(attack_values) - 1, 0, -1):
            if attack_values[i] >= math.ceil(len(self.bugList) / 2):
                self.attack = i
                return i
            attack_values[i - 1] += attack_values[i]
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
            bug.state = "to move"

        for bug in self.bugList:
            bug.setMove(bug.move - 1)
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

    def setMoves(self):
        moves = 20
        for bug in self.bugList:
            if moves > bug.move:
                moves = bug.move
        self.numberOfMoves = moves
