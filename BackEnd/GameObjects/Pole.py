from Util.PlayerEnum import PlayerEnum


class Pole:
    def __init__(self, q, r, s, size):
        self.q = q
        self.r = r
        self.s = s
        self.resources = False
        self.is_white_hatchery = False
        self.is_black_hatchery = False
        self.hatcheryID = None
        self.size = size

        self.bug = None

        self.WN = None
        self.EN = None
        self.E = None
        self.ES = None
        self.WS = None
        self.W = None

    def getNeighbours(self):
        return [self.WN, self.EN, self.E, self.ES, self.WS, self.W]

    def getDictionary(self):
        direction = {
            "WN" : self.WN,
            "EN" : self.EN,
            "E" : self.E,
            "ES" : self.ES,
            "WS" : self.WS,
            "W" : self.W
        }
        return direction

    def setHatchery(self, isHa, hatcheryID, side):
        if side == PlayerEnum.B:
            self.is_white_hatchery = isHa
        elif side == PlayerEnum.C:
            self.is_black_hatchery = isHa
        self.hatcheryID = hatcheryID

    def setBug(self, bug):
        self.bug = bug
        bug.setField(self)

    def resetBug(self):
        if self.bug is not None:
            self.bug.setField(None)
            self.bug = None

    def setResources(self, isRes):
        self.resources = isRes

    def setWN(self, Pole):
        self.WN = Pole

    def setEN(self, Pole):
        self.EN = Pole

    def setE(self, Pole):
        self.E = Pole

    def setES(self, Pole):
        self.ES = Pole

    def setWS(self, Pole):
        self.WS = Pole

    def setW(self, Pole):
        self.W = Pole

    def toString(self):
        return "[" + str(self.q - self.size) + "," + str(self.r - self.size) + "," + str(self.s - self.size) + "]"

    def cor(self):
        return [self.q,self.r,self.s]