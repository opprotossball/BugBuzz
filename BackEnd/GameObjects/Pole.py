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
        self.banned = False

        self.bug = None

    def set_hatchery(self, hatcheryID, side):
        if side == PlayerEnum.B:
            self.is_white_hatchery = True
        elif side == PlayerEnum.C:
            self.is_black_hatchery = True
        self.hatcheryID = hatcheryID

    def set_resources(self, is_res):
        self.resources = is_res

    def set_bug(self, bug):
        self.bug = bug
        bug.set_field(self)

    def reset_bug(self):
        if self.bug is not None:
            self.bug.set_field(None)
            self.bug = None

    def cor(self):
        return [self.q, self.r, self.s]

    def coordinates_to_string(self):
        return "(" + str(self.q) + "," + str(self.r) + "," + str(self.s) + ")"

    def __str__(self):
        return self.coordinates_to_string()

    def __repr__(self):
        return self.coordinates_to_string()
