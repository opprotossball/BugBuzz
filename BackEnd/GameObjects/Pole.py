from Util.PlayerEnum import PlayerEnum


class Pole:
    def __init__(self, q, r, s, size, board):
        self.q = q
        self.r = r

        self.x = q
        self.y = r

        self.board = board

        self.s = s
        self.resources = False
        self.is_white_hatchery = False
        self.is_black_hatchery = False
        self.hatcheryID = None
        self.size = size

        self.bug = None


    def setHatchery(self, hatcheryID, side):
        if side == PlayerEnum.B:
            self.is_white_hatchery = True
        elif side == PlayerEnum.C:
            self.is_black_hatchery = True
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

    def toString(self):
        return "[" + str(self.q - self.size) + "," + str(self.r - self.size) + "," + str(self.s - self.size) + "]"

    def cor(self):
        return [self.q, self.r, self.s]

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"
