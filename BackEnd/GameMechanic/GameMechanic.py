import math
from queue import PriorityQueue
from random import randint

from BackEnd.GameObjects.Armia import Armia
from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameObjects.Pole import Pole
from BackEnd.GameObjects.Robal import States
from FrontEnd.Display import Display
from FrontEnd.UI import UI
from Util import Information
from Util.PlayerEnum import PlayerEnum


class GameMechanic:
    def __init__(self):
        self.board = Plansza(Information.board_size)
        self.BlackPlayer = None
        self.WhitePlayer = None

    def get_player(self, side):
        if side == PlayerEnum.B:
            return self.WhitePlayer
        elif side == PlayerEnum.C:
            return self.BlackPlayer
        else:
            return

    def getArmies(self, side):
        armies = []
        bugs = self.get_player(side).bugList
        for bug in bugs:
            if bug.army not in armies:
                armies.append(self.get_cluster_army(bug.field))

    def get_cluster_army(self, pole):
        if pole.bug is None:
            return

        org_side = pole.bug.side

        army = Armia(self.board)

        claster = [pole]
        self.__add_to_claster(claster, pole, org_side)

        for pole in claster:
            army.addBug(pole.bug)

    def __add_to_claster(self, claster, pole, side):
        pola = self.board.get_field_neighs(pole)

        for pole_x in pola:
            if pole_x is not None and pole_x not in claster:
                if pole_x.bug is not None and pole_x.bug.side == side:
                    claster.append(pole_x)
                    self.__add_to_claster(claster, pole_x, side)

    def reset_moves_for_bugs(self, side):
        player = self.get_player(side)

        for bug in player.bugList:
            bug.setMove(bug.max_move)

    def setMoves(self, army):
        moves = 20
        for bug in army.bugList:
            if moves > bug.move:
                moves = bug.move
        army.numberOfMoves = moves

    def getValidMoves(self, army):
        for bug in army.bugList:
            bug.moveToExamine = Information.directionOptions.copy()
            bug.validMoves = []
            bug.invalidMoves = []

        queue = PriorityQueue()

        for bug in army.bugList:
            queue.put((6, bug))

        while not queue.empty():
            priority, bug = queue.get()
            move_to_examine = bug.moveToExamine.copy()
            for name_of_direction in bug.moveToExamine:
                neighbour = self.board.get_field_neigh(bug.field, name_of_direction)
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

        for bug in army.bugList:
            for move in bug.validMoves:
                if move not in armyValidMoves:
                    armyValidMoves.append(move)
                if armyValidMoves == Information.directionOptions:
                    return armyValidMoves
        return armyValidMoves

    def performeMove(self, army, direction):
        bug_list = army.bugList

        for bug in bug_list:
            bug.state = States.ToMove

        for bug in bug_list:
            bug.setMove(bug.move - 1)
            if bug.state == States.ToMove:
                field = self.board.get_field_neigh(bug.field, direction)
                if bug.hasEnemyInSurrounding():
                    bug.state = States.WontMove
                elif field is not None:
                    if field.bug is None:
                        bug.moveBugTo(field)
                        bug.state = States.Moved
                    elif field.bug.state == States.WontMove:
                        bug.state = States.WontMove
                else:
                    bug.state = States.WontMove

        army.numberOfMoves -= 1

    def get_attacks(self, army):
        attackArray = []
        for bug in army.bugList:
            for neighbour in bug.field.getNeighbours():
                if self.OnThisSide(bug.side, neighbour):
                    if neighbour.bug.army in attackArray:
                        continue
                    else:
                        attackArray.append(neighbour.bug.army)
        return attackArray

    def get_attack_power_and_bugs_attacked(self, attacked_army):
        attacking_bugs = set()
        attacking_armies = set()
        attacked_bugs = set()
        for bug in attacked_army.bugList:
            neighs = self.board.get_field_neighs(bug.field)
            for neighbour in neighs:
                if self.OnThisSide(bug.side, neighbour):
                    attacking_bugs.add(neighbour.bug)
                    attacking_armies.add(neighbour.bug.army)
                    attacked_bugs.add(bug)
        power = len(attacking_bugs)
        for army in attacking_armies:
            power += self.calculate_attack(army)
        return power, attacked_bugs

    def calculate_attack(self, army):
        attack_values = [0 for i in range(6)]
        for bug in army.bugList:
            attack_values[bug.attack] += 1
        for i in range(len(attack_values) - 1, 0, -1):
            if attack_values[i] >= math.ceil(len(army.bugList) / 2):
                self.attack = i
                return i
            attack_values[i - 1] += attack_values[i]
        self.attack = 0
        return 0

    def rollDice(self, diceCount):
        rollArray = [randint(1, 10) for i in range(diceCount)]
        return rollArray
    def getToughnessArray(self, army):
        toughnessInterval = []
        for bug in army.bugList:
            newElement = bug.toughness
            if newElement in toughnessInterval:
                continue
            else:
                toughnessInterval += newElement
        return toughnessInterval

    def getResourcesForSide(self, side):
        resources = self.board.resources
        for pole in self.board.resources:
            self.get_cluster_army(pole)

        n = 1
        for field in resources:
            if field.bug is not None and field.bug.side == side:
                n += field.bug.army.numberOfGrassHoppers
        return n

    def getAvailableSpaceForHatch(self, side):
        hatchery = []
        if side == PlayerEnum.B:
            hatchery = self.board.whitesHatchery
        elif side == PlayerEnum.C:
            hatchery = self.board.blacksHatchery
        option = []
        for hatch in hatchery:
            if hatch.bug is not None:
                option.append(hatch)
        return option

    def OnThisSide(self, ourSide, neighbourField):
        return neighbourField is not None and neighbourField.bug is not None and neighbourField.bug.side is not ourSide

    def updateWindow(self):
        if self.display is not None:
            self.display.update_window()

    def setGUI(self):
        self.ui = UI(self)
        self.display = Display(self)

    def setDisplay(self):
        self.display = Display(self)
