import math
from random import randint
from BackEnd.GameObjects.Armia import Armia
from BackEnd.GameObjects.Robal import States
from FrontEnd.Display import Display
from FrontEnd.UI import UI
from Util.PlayerEnum import PlayerEnum


class GameMechanic:
    def __init__(self):
        self.board = None
        self.BlackPlayer = None
        self.WhitePlayer = None
        self.display = None
        self.ui = None

    def get_player(self, side):
        if side == PlayerEnum.B:
            return self.WhitePlayer
        elif side == PlayerEnum.C:
            return self.BlackPlayer
        else:
            return

    def set_player(self, player):
        if player.side == PlayerEnum.B:
            self.WhitePlayer = player
        else:
            self.BlackPlayer = player

    def set_board(self, board):
        self.board = board

    def get_armies(self, side, player=None):
        armies = []
        bugs = self.get_player(side).bugList
        for bug in bugs:
            if bug.army not in armies:
                self.get_cluster_army(bug.field)
                armies.append(bug.army)
        for army in armies:
            self.set_moves(army)
        return armies

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

    def set_moves(self, army):
        moves = 20
        for bug in army.bugList:
            if moves > bug.move:
                moves = bug.move
        army.numberOfMoves = moves

    def perform_move(self, army, direction):
        bug_list = army.bugList

        for bug in bug_list:
            bug.state = States.ToMove

        for bug in bug_list:
            bug.set_move(bug.move - 1)
            if bug.state == States.ToMove:
                field = self.board.get_field_neigh(bug.field, direction)
                if bug.has_enemy_in_surrounding():
                    bug.state = States.WontMove
                elif field is not None:
                    if field.bug is None:
                        bug.move_bug_to(field)
                        bug.state = States.Moved
                    elif field.bug.state == States.WontMove:
                        bug.state = States.WontMove
                else:
                    bug.state = States.WontMove

        army.numberOfMoves -= 1

    def get_attacks(self, army):
        attack_array = []
        for bug in army.bugList:
            for neighbour in bug.field.getNeighbours():
                if self.has_opponents_neighbour(bug.side, neighbour):
                    if neighbour.bug.army in attack_array:
                        continue
                    else:
                        attack_array.append(neighbour.bug.army)
        return attack_array

    def get_attack_power_and_bugs_attacked(self, attacked_army):
        attacking_bugs = set()
        attacking_armies = set()
        attacked_bugs = set()
        for bug in attacked_army.bugList:
            neighs = self.board.get_field_neighs(bug.field)
            for neighbour in neighs:
                if self.has_opponents_neighbour(bug.side, neighbour):
                    attacking_bugs.add(neighbour.bug)
                    attacking_armies.add(neighbour.bug.army)
                    attacked_bugs.add(bug)
        power = len(attacking_bugs)
        for army in attacking_armies:
            power += self.calculate_attack(army)
        return power, attacked_bugs

    def calculate_attack(self, army):
        attack_values = [0 for _ in range(6)]
        for bug in army.bugList:
            attack_values[bug.attack] += 1
        for i in range(len(attack_values) - 1, 0, -1):
            if attack_values[i] >= math.ceil(len(army.bugList) / 2):
                return i
            attack_values[i - 1] += attack_values[i]
        return 0

    def roll_dice(self, dice_count):
        roll_array = [randint(1, 10) for i in range(dice_count)]
        return roll_array

    def get_toughness_array(self, army):
        toughness_interval = []
        for bug in army.bugList:
            for newElement in bug.toughness:
                if newElement in toughness_interval:
                    continue
                else:
                    toughness_interval.append(newElement)
        return sorted(toughness_interval)

    def set_army_on_tile(self, tile):
        bug = tile.bug
        if bug is not None:
            army = Armia(self.board)
            army.addBug(bug)
            bug.recruit_neighbours()
            self.set_moves(army)
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
        for pole in self.board.resources:
            self.get_cluster_army(pole)

        n = 1
        for field in resources:
            if field.bug is not None and field.bug.side == side:
                n += field.bug.army.numberOfGrassHoppers
        return n

    def get_available_space_for_hatch(self, side):
        hatchery = []
        if side == PlayerEnum.B:
            hatchery = self.board.whitesHatchery
        elif side == PlayerEnum.C:
            hatchery = self.board.blacksHatchery
        option = []
        for hatch in hatchery:
            if hatch.bug is None:
                option.append(hatch)
        return option

    def has_opponents_neighbour(self, our_side, neighbour_field):
        return neighbour_field is not None and neighbour_field.bug is not None and neighbour_field.bug.side is not our_side

    def update_window(self):
        if self.display is not None:
            self.display.update_window()

    def reset_move(self, side):
        if side == PlayerEnum.B:
            player = self.WhitePlayer
        elif side == PlayerEnum.C:
            player = self.BlackPlayer
        else:
            print(side + "is not a valid side")
            return False
        for bug in player.bugList:
            bug.set_move(bug.max_move)

    def set_new_ui_and_display(self):
        self.ui = UI(self)
        self.display = Display(self)

    def set_display(self):
        self.display = Display(self)

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
