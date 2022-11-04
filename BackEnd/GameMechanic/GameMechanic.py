from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameObjects.Trader import Trader
from FrontEnd.UI import UI
from FrontEnd.Display import Display
from BackEnd.GameObjects.Armia import Armia
from Util import Information


def concatenate_moves(table1, table2):
    concatenated = []
    for el1 in table1:
        for el2 in table2:
            concatenated.append((el1, el2))
    return concatenated


class GameMechanic:
    def __init__(self):
        self.BlackPlayer = None
        self.WhitePlayer = None

        self.board = Plansza(Information.board_size)

    def getArmies(self, player):
        armies = []

        for bug in player.bugList:
            bug.army = None

        for bug in player.bugList:
            if bug.army is not None:
                continue
            army = Armia()
            army.addBug(bug)
            bug.recruitNeighbours()
            armies.append(army)

        return armies

    def getResourcesForPlayer(self, player):
        resources = self.board.resources
        self.getArmies(player)
        n = 1
        for field in resources:
            if field.bug is not None and field.bug.side == player.side:
                n += field.bug.army.numberOfGrassHoppers
        return n

    def isAvailableSpaceForHatch(self, side, board):
        hatchery = []
        if side == "B":
            hatchery = board.whitesHatchery
        elif side == "C":
            hatchery = board.blacksHatchery
        for hatch in hatchery:
            if hatch.bug is None:
                return True
        return False

    def getMovesForPlayer(self, player):
        armies = self.getArmies(player)
        moves = []
        for army in armies:
            if army.numberOfMoves <= 0:
                continue
            moves += concatenate_moves([army], army.getValidMoves())
        moves.append("end")
        return moves

    def performMove(self, army, direction):
        army.performMove(direction)

    def getAttacksForPlayer(self, player):
        armies = self.getArmies(self.oppositeSide(player.side))
        attacks = []
        for army in armies:
            if army.hasAttack():
                attacks += army
        attacks.append("end")
        return attacks

    def performAttack1(self):
        pass

    def performAttack2(self):
        pass

    def getHatchForPlayer(self, player):
        hatchery_field = self.getAvailableSpaceForHatch(player)

        trader = Trader()
        possible_to_hatch = trader.getOptions(player)

        options = concatenate_moves(hatchery_field, possible_to_hatch)
        options.append("end")
        return options

    def performHatch(self, player, hatchery_field, option):
        trader = Trader()
        bug = trader.buyBug(player, option)
        bug.moveBugTo(hatchery_field)

    def getAvailableSpaceForHatch(self, player):
        hatchery = self.getHatcheryForPlayer(player)
        option = []
        for hatch in hatchery:
            if hatch.bug is None:
                option.append(hatch)
        return option

    def getHatcheryForPlayer(self, player):
        if player.side == "B":
            return self.board.whitesHatchery
        elif player.side == "C":
            return self.board.blacksHatchery

    def getResourcesForPlayer(self, player):
        n = 1
        for field in self.board.resources:
            if field.bug is not None and field.bug.side == player.side:
                n += field.bug.army.numberOfGrassHoppers
        return n

    def reset_move_left(self, armies):
        for army in armies:
            army.setMove()

    def oppositeSide(self, side):
        if side == "B":
            return self.BlackPlayer
        else:
            return self.WhitePlayer

    def gameIsOver(self, board):
        bug = board.resources[0].bug
        if bug is not None:
            side = bug.side
        else:
            return False

        for pole in board.resources:
            if pole.bug is None or pole.bug.side != side:
                return False

        self.winner_side = side
        return True

    def setGUI(self):
        self.UI = UI(self)
        self.display = Display(self)

    def setDisplay(self):
        self.display = Display(self)

    def updateWindow(self):
        if self.display is not None:
            self.display.updateWindow()
