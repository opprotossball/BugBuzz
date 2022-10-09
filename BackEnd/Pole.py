class Pole:
    def __init__(self, q, r, s, size):
        self.bug = None
        self.q = q
        self.r = r
        self.s = s
        self.resources = False
        self.hatchery = False
        self.size = size
        self.iterating_list = [self.WN, self.W, self.WS, self.ES, self.E, self.EN]

        self.direction = {
            "WN" : self.WN,
            "EN" : self.EN,
            "E" : self.E,
            "ES" : self.ES,
            "WS" : self.WS,
            "W" : self.W
        }

        self.neighbours = [self.WN, self.EN, self.E, self.ES, self.WS, self.W]
        self.directions = ['WN', 'EN', 'E', 'ES', 'WS', 'W']

    def setHatchery(self, isHa, hatcheryID):
        self.hatchery = isHa
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