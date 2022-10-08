from time import sleep

from Trader import Trader


class InterfejsGracza:
    def __init__(self, side, GM):
        self.GM = GM
        self.side = side
        self.Armies = []
        self.resources = 0

    def addResources(self):
        self.resource += 1
        for army in self.Armies:
            self.resources += army.getNumberOfResources()

    def Attack(self):
        ids = self.getArmiesID()
        print(ids)
        while len(ids) > 0:
            input = input()
            while input not in ids:
                input = input()
            army = self.getAmryByID(input)
            while army.hasAttack():
                print(army.getAttacks)
                while input not in army.getAttacks:
                    input = input()
                army.performeAttack(input)

    def getArmiesID(self):
        id = []
        for army in self.Armies:
            id.append(army.id)
        return id

    def getAmryByID(self, id):
        for army in self.Armies:
            if army.id == id:
                return army

    def Moves(self):
        ids = self.getArmiesID()
        print(ids)
        while len(ids) > 0:
            input = input()
            while input not in ids:
                input = input()
            army = self.getAmryByID(input)
            while army.hasMove():
                print(army.getMoves)
                while input not in army.getMoces():
                    input = input()
                army.performeMoves(input)
                army.resetArmy()

    def getArmysMoves(self, army):
        moves = [army.id, army.numberOfMoves, []]
        for move in army.validMoves():
            moves[2].append(move)
        return moves

    def Hatch(self):
        trader = Trader()  # If want to change prices of the Robale we need to to this here
        options = trader.getOptions(self.resources)
        while len(options) > 1 or self.GM.isAvialabelSpaceForHatch(self.side):
            options = trader.getOptions(self.resources)
            print(options)
            selectedOption = input()
            while selectedOption not in options:
                selectedOption = input()
            if selectedOption == 4:
                break

            placementOptionField = self.GM.GetAvialabelSpaceForHatch(self.side)
            placementOptionID = []
            selectPlacementField = 0
            for filed in placementOptionField:
                placementOptionID.append(filed.hatcheryID)
            if len(placementOptionField) == 1:
                selectPlacementField = placementOptionField[0]
            else:
                selectPlacement = input()
                while selectPlacement not in placementOptionID:
                    selectPlacementField = input()
            bug, price = trader.buyBug(selectedOption, self.resources)
            self.resources -= price
            self.GM.addBug(selectPlacementField, bug)

            # Replace input() with some getter to AI

