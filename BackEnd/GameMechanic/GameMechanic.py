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
            bugs = self.WhitePlayer.bugList
        elif side == PlayerEnum.C:
            bugs = self.BlackPlayer.bugList
        else:
            return

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
        if side == PlayerEnum.B:
            player = self.WhitePlayer
        elif side == PlayerEnum.C:
            player = self.BlackPlayer
        else:
            print(side + "is not a valid side")
            return False

        for bug in player.bugList:
            bug.setMove(bug.max_move)

    def getResourcesForSide(self, side):
        resources = self.board.resources
        for pole in self.board.resources:
            self.get_cluster_army(pole)

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
