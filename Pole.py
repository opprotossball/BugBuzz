class Pole:
    def __init__(self, q, r, s, size):
        self.q = q
        self.r = r
        self.s = s
        self.resources = False
        self.hatchery = False
        self.size = size

    def setHatchery(self, isHa):
        self.hatchery = isHa

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
