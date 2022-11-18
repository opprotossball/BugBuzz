from BackEnd.GameMechanic.Player import PlayerState
from FrontEnd.Button import Button
import pygame


class UI:
    def __init__(self, game_master):
        self.tile_buttons = []
        self.hatch_buttons = []
        self.game_master = game_master
        self.selected_tile = None
        self.chosen_to_hatch = None
        self.mode = None
        self.side = None
        self.player = None
        self.rolls = None
        self.attacking = False

        self.ant_white_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/antWhiteHatchButton.png")
        self.grasshooper_white_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperWhiteHatchButton.png")
        self.spider_white_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/spiderWhiteHatchButton.png")
        self.beetle_white_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/beetleWhiteHatchButton.png")

        self.ant_white_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/antWhiteSelectedHatchButton.png")
        self.grasshooper_white_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperWhiteSelectedHatchButton.png")
        self.spider_white_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/spiderWhiteSelectedHatchButton.png")
        self.beetle_white_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/beetleWhiteSelectedHatchButton.png")

        self.ant_black_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/antBlackHatchButton.png")
        self.grasshooper_black_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperBlackHatchButton.png")
        self.spider_black_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/spiderBlackHatchButton.png")
        self.beetle_black_hatch_button = pygame.image.load("./FrontEnd/Assets/Buttons/beetleBlackHatchButton.png")

        self.ant_black_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/antBlackSelectedHatchButton.png")
        self.grasshooper_black_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperBlackSelectedHatchButton.png")
        self.spider_black_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/spiderBlackSelectedHatchButton.png")
        self.beetle_black_hatch_button_selected = pygame.image.load("./FrontEnd/Assets/Buttons/beetleBlackSelectedHatchButton.png")

        end_phase_button_image = pygame.image.load("./FrontEnd/Assets/Buttons/endPhaseButton.png")
        end_phase_button_selected_image = pygame.image.load("./FrontEnd/Assets/Buttons/endPhaseSelectedButton.png")

        self.end_phase_button = Button(end_phase_button_image, end_phase_button_selected_image, 0.2)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.phase_titles = {
            0: "White's combat phase",
            1: "White's move phase",
            2: "White's hatch phase",
            3: "Black's combat phase",
            4: "Black's move phase",
            5: "Black's hatch phase"
        }

        self.tip_texts = [
            "Select opponent's army to attack"
            "Select and move your army"
            "Hatch bug in your hatchery"
            "Wait for opponent to play"
            "Wait for opponent to play"
            "Wait for opponent to play"
        ]

    def setMode(self, mode, side):
        self.mode = mode
        self.side = side
        hatch_buttons = []
        if side == "B":
            self.player = self.game_master.WhitePlayer
            hatch_buttons.append(Button(self.ant_white_hatch_button, self.ant_white_hatch_button_selected, None, "M"))
            hatch_buttons.append(Button(self.grasshooper_white_hatch_button, self.grasshooper_white_hatch_button_selected, None, "K"))
            hatch_buttons.append(Button(self.spider_white_hatch_button, self.spider_white_hatch_button_selected, None, "P"))
            hatch_buttons.append(Button(self.beetle_white_hatch_button, self.beetle_white_hatch_button_selected, None, "Z"))
        elif side == "C":
            self.player = self.game_master.BlackPlayer
            hatch_buttons.append(Button(self.ant_black_hatch_button, self.ant_black_hatch_button_selected, None, "M"))
            hatch_buttons.append(Button(self.grasshooper_black_hatch_button, self.grasshooper_black_hatch_button_selected, None, "K"))
            hatch_buttons.append(Button(self.spider_black_hatch_button, self.spider_black_hatch_button_selected, None, "P"))
            hatch_buttons.append(Button(self.beetle_black_hatch_button, self.beetle_black_hatch_button_selected, None, "Z"))
        self.hatch_buttons = hatch_buttons

    def setTileButtons(self, tilebutons):
        self.tile_buttons = tilebutons

    def selectArmy(self, tile):
        tiles = []
        bug = tile.bug
        if bug is not None and bug.army is not None:
            for anotherBug in bug.army.bugList:
                tiles.append(anotherBug.field)
        return tiles

    def getInput(self):
        if self.mode == PlayerState.HATCH:
            for hatchButton in self.hatch_buttons:
                hatchButton.isClickedLeft()
                if hatchButton.isSelected():
                    self.chosen_to_hatch = hatchButton.bugShortName

        for tile_button in self.tile_buttons:
            if tile_button.isClickedLeft():
                tile = tile_button.tile
                bug = tile.bug

                if self.mode == PlayerState.COMBAT:
                    if bug is not None and bug.side != self.side:
                        if self.player.kills > 0:
                            self.player.kill_bug(bug)
                            if self.player.kills == 0:
                                self.game_master.display.highlightedTiles = []
                            return
                        else:
                            was_attacked, kills, rolls = self.player.perform_attack(bug.army)
                            if was_attacked:
                                self.attacking = True
                                self.game_master.display.highlightedTiles = self.selectArmy(tile)
                                self.game_master.display.highlightedColor = (150, 45, 45)
                                self.rolls = rolls
                                return
                    elif self.player.kills > 0 and self.player.attacked_bugs.__len__() > 0:
                        return  # killing is compulsory for now
                    else:
                        self.attacking = False

                elif self.mode == PlayerState.MOVE:
                    if bug is None:
                        if self.makeMove(tile):
                            return
                    self.selected_tile = None

                elif self.mode == PlayerState.HATCH:
                    if self.chosen_to_hatch is not None:
                        if self.player.perform_hatch(self.chosen_to_hatch, tile):
                            self.chosen_to_hatch = None
                            return

                selected_army_tiles = self.selectArmy(tile)
                self.game_master.display.highlightedTiles = selected_army_tiles
                self.game_master.display.highlightedColor = (81, 210, 252)

                if self.mode == PlayerState.MOVE:
                    if tile is not None and bug is not None and bug.side == self.side:
                        self.selected_tile = tile

        if self.mode != PlayerState.MOVE:
            self.selected_tile = None

        if self.mode != PlayerState.INACTIVE:
            if self.end_phase_button.isClickedLeft():
                self.game_master.display.highlightedTiles = []
                self.attacking = False
                self.player.end_phase()

    def makeMove(self, tile):
        if self.selected_tile is None:
            self.selected_tile = None
            return False
        dictionary = self.selected_tile.getDictionary()
        directions = [d for d, n in dictionary.items() if n == tile]
        if directions.__len__() == 0:
            self.selected_tile = None
            return False
        direction = directions[0]
        leader = self.selected_tile.bug
        self.selected_tile = leader.field
        self.player.perform_move(leader.army, direction)
        move_performed = self.game_master.display.highlightedTiles = self.selectArmy(tile)
        self.selected_tile = leader.field
        return move_performed

    def get_count_of_bugs_available(self):
        if self.side == "B":
            color = self.WHITE
        else:
            color = self.BLACK
        return self.player.bugs_available, color

    def get_number_of_resources(self):
        if self.side == "B":
            color = self.WHITE
        else:
            color = self.BLACK
        return self.player.resources, color

    def get_phase_title(self):
        turn = self.game_master.turn
        if turn < 3:
            color = self.WHITE
        else:
            color = self.BLACK
        return self.phase_titles[turn], color

    def get_combat_results(self):
        if not self.attacking:
            return None, None
        turn = self.game_master.turn
        if turn < 3:
            color = self.WHITE
        else:
            color = self.BLACK
        text = "Your rolls were: {}\n Kill {} bug".format(self.rolls, self.player.kills)
        if self.player.kills != 1:
            text += "s"
        return text, color
