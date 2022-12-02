from random import randint

from BackEnd.GameObjects.Armia import Armia
from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameObjects.Pole import Pole
from FrontEnd.Display import Display
from FrontEnd.UI import UI
from Util import Information
from Util.PlayerEnum import PlayerEnum


class GameMechanic:
    def __init__(self):
        self.board = Plansza(Information.board_size)
        self.BlackPlayer = None
        self.WhitePlayer = None

    def getArmies(self, side):
        armies = []

        if side == PlayerEnum.B:
            player = self.WhitePlayer
        elif side == PlayerEnum.C:
            player = self.BlackPlayer
        else:
            return

        for bug in player.bugList:
            bug.army = None


        for bug in player.bugList:
            if bug.army not in armies:
                army1 = self.get_cluster_army(bug.field)
                armies.append(army1)

        return armies

    def updateArmy(self, pole):
        army = pole.bug.army
        if army is None:
            self.getArmies(pole.bug.side)
            return

        armies = []
        for bug in army.bugList:
            if bug.army not in armies:
                army1 = self.get_cluster_army(pole)
                armies.append(army1)

    def get_cluster_army(self, pole):
        if pole.bug is None:
            return

        org_side = pole.bug.side

        army = Armia(self.board)

        claster = []
        self._add_to_claster(claster, pole, org_side)

        claster.append(pole)
        for pole in claster:
            army.addBug(pole.bug)

        return army


    def _add_to_claster(self, claster, pole, side):
        pola = self.board.get_field_neighs(pole)

        for pole_x in pola:
            if pole_x is not None and pole_x not in claster:
                if pole_x.bug is not None and pole_x.bug.side == side:
                    claster.append(pole_x)
                    self._add_to_claster(claster, pole_x, side)

    def getResourcesForSide(self, side):
        resources = self.board.resources
        self.getArmies(side)
        n = 1
        for field in resources:
            if field.bug is not None and field.bug.side == side:
                n += field.bug.army.numberOfGrassHoppers
        return n

    def isAvailableSpaceForHatch(self, side):
        hatchery = []
        if side == PlayerEnum.B:
            hatchery = self.board.whitesHatchery
        elif side == PlayerEnum.C:
            hatchery = self.board.blacksHatchery
        for hatch in hatchery:
            if hatch.bug is None:
                return True
        return False

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

    def resetMove(self, side):
        if side == PlayerEnum.B:
            player = self.WhitePlayer
        elif side == PlayerEnum.C:
            player = self.BlackPlayer
        else:
            print(side + "is not a valid side")
            return False
        for bug in player.bugList:
            bug.setMove(bug.max_move)

    def setGUI(self):
        self.ui = UI(self)
        self.display = Display(self)

    def setDisplay(self):
        self.display = Display(self)

    def rollDice(self, diceCount):
        rollArray = [randint(1, 10) for i in range(diceCount)]
        return rollArray

    def updateWindow(self):
        if self.display is not None:
            self.display.update_window()

    def isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(self, ourSide, neighbourField):
        return neighbourField is not None and neighbourField.bug is not None and neighbourField.bug.side is not ourSide

    def get_attack_power_and_bugs_attacked(self, attacked_army):
        attacking_bugs = set()
        attacking_armies = set()
        attacked_bugs = set()
        for bug in attacked_army.bugList:
            for neighbour in bug.field.getNeighbours():
                if self.isNotNoneAndHasABugAndThisBugIsNotOnThissBugSide(bug.side, neighbour):
                    attacking_bugs.add(neighbour.bug)
                    attacking_armies.add(neighbour.bug.army)
                    attacked_bugs.add(bug)
        power = len(attacking_bugs)
        for army in attacking_armies:
            power += army.calculate_attack()
        return power, attacked_bugs
