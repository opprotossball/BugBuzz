from random import randint

from FrontEnd.UI import UI
from FrontEnd.Display import Display
from BackEnd.GameObjects.Armia import Armia
from BackEnd.GameObjects.Plansza import Plansza
from Util import Information


class GameMechanic:
    def __init__(self):
        self.board = None
        self.BlackPlayer = None
        self.WhitePlayer = None

    def set_player(self, player):
        if player.side == 'B':
            self.WhitePlayer = player
        else:
            self.BlackPlayer = player

    def set_board(self, board):
        self.board = board

    def get_armies(self, side, player=None):
        armies = []

        if player is not None:
            player = player
        else:
            if side == "B":
                player = self.WhitePlayer
            elif side == "C":
                player = self.BlackPlayer
            else:
                return

        for bug in player.bugList:
            bug.army = None

        for bug in player.bugList:
            if bug.army is not None:
                continue
            army = Armia()
            army.addBug(bug)
            bug.recruitNeighbours()
            army.setMoves()
            armies.append(army)

        return armies

    def set_army_on_tile(self, tile):
        bug = tile.bug
        if bug is not None:
            army = Armia()
            army.addBug(bug)
            bug.recruitNeighbours()
            army.setMoves()
            return army
        else:
            return None
    def set_player_bugs(self, board, player):
        player.bugList = []
        for tile in board.iterList:
            bug = tile.bug
            if bug is not None and bug.side == player.side:
                player.bugList.append(bug)

    def get_resources_for_side(self, side):
        resources = self.board.resources
        self.get_armies(side)
        n = 1
        for field in resources:
            if field.bug is not None and field.bug.side == side:
                n += field.bug.army.numberOfGrassHoppers
        return n

    def isAvailableSpaceForHatch(self, side):
        hatchery = []
        if side == "B":
            hatchery = self.board.whitesHatchery
        elif side == "C":
            hatchery = self.board.blacksHatchery
        for hatch in hatchery:
            if hatch.bug is None:
                return True
        return False

    def getAvailableSpaceForHatch(self, side):
        hatchery = []
        if side == "B":
            hatchery = self.board.whitesHatchery
        elif side == "C":
            hatchery = self.board.blacksHatchery
        option = []
        for hatch in hatchery:
            if hatch.bug is None:
                option.append(hatch)
        return option

    def reset_move(self, side):
        if side == "B":
            player = self.WhitePlayer
        elif side == "C":
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

    def set_position_for_player(self, board, player, delete_others=True):  # bugs controlled by other player are unchanged
        if delete_others:
            for tile in board.iterList:
                if tile.bug is not None and tile.bug.side == player.side:
                    tile.bug = None
        for bug in player.bugList:
            bug.field.bug = bug

    def change_position_for_player(self, old_player, new_player):
        for bug in old_player.bugList:
            bug.field.bug = None
        for bug in new_player.bugList:
            bug.field.bug = bug
