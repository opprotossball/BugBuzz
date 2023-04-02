import random
from abc import abstractmethod

from AI_module.AproxBotDefaultWeights import default_weights
from BackEnd.GameMechanic.Player import Player, PlayerState
from BackEnd.GameMechanic.PositionGenerator import PositionGenerator
from BackEnd.GameObjects.Trader import Trader
from Util import Information


class AproxBot(Player):
    def __init__(self, gm, side):
        super().__init__(gm, side)
        self.generator = PositionGenerator()
        self.trader = Trader()
        self.weights = default_weights

    def set_state(self, state):
        self.state = state

    def play(self):
        if self.state == PlayerState.INACTIVE:
            return
        elif self.state == PlayerState.COMBAT:
            self.hatch()
        elif self.state == PlayerState.MOVE:
            self.perform_moves()
        elif self.state == PlayerState.HATCH:
            self.attack_and_kill_randomly()
        self.end_phase()

    @abstractmethod
    def get_score(self):
        pass

    def n_of_resources(self):
        return self.gm.get_resources_for_side(self.side)

    def perform_moves(self):
        armies_to_move = self.gm.get_armies(self.side)
        count = 0
        while armies_to_move and count < 30:
            count += 1
            best = self.get_best_move(armies_to_move)
            if best is None:
                return
            self.perform_move(best[1].bug.army, best[2])
            armies_to_move = [army for army in self.gm.get_armies(self.side) if army.numberOfMoves > 0]

    def get_best_move(self, armies):
        moves = []
        tiles = [army.bugList[0].field for army in armies]
        for tile in tiles:
            for direction in Information.directionOptions:
                player = self.clone_for_move()
                self.gm.set_player(player)
                self.gm.change_position_for_player(self, player)
                self.gm.get_armies(self.side)
                if tile.bug is None:  # nie powinno być konieczne
                    self.gm.change_position_for_player(player, self)
                    self.gm.set_player(self)
                    continue
                army = tile.bug.army
                player.perform_move(army, direction)
                moves.append((player.get_score(), tile, direction))
                self.gm.change_position_for_player(player, self)
                self.gm.set_player(self)
                del player
        if not moves:
            return None
        return max(moves, key=lambda x: x[0])

    def attack_and_kill_randomly(self):
        for army in self.gm.get_armies(self.get_opponent_side()):
            if self.perform_attack(army) is None:
                return
            while True:
                if not self.attacked_bugs or not self.kill_bug(random.sample(self.attacked_bugs, 1)[0]):
                    break

    def hatch(self, prefered=None):
        options = self.trader.get_options(self.resources, self.bugs_available)
        hatchery = self.gm.get_available_space_for_hatch(self.side)
        while options and hatchery:
            if prefered is None:
                to_hatch = random.choice(options)
            else:
                for bug_type in prefered:
                    if bug_type in options:
                        to_hatch = bug_type
                        break
            self.perform_hatch(to_hatch, random.choice(hatchery))
            options = self.trader.get_options(self.resources, self.bugs_available)
            hatchery = self.gm.get_available_space_for_hatch(self.side)

    def get_avg_attack(self):
        attacks = [self.gm.calculate_attack(army) for army in self.gm.get_armies(self.side)]
        return sum(attacks) / len(attacks)

    def get_avg_toughness(self):
        toughs = [len(self.gm.get_toughness_array(army)) for army in self.gm.get_armies(self.side)]
        return sum(toughs) / len(toughs)

    def clone_for_move(self):
        new = self.__class__(self.gm, self.side)
        for bug in self.bugList:
            new.bugList.append(bug.clone_with_field())
        return new
