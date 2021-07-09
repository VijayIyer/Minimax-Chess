class Position:
    def __init__(self, pos):
        self.row = pos[0]
        self.col = pos[1]


class Move:
    def __init__(self, prev, new_pos):
        self.prev = prev
        self.new_pos = new_pos


class En_passant(Move):
    def __init__(self, prev, new_pos):
        super(En_passant, self).__init__(prev, new_pos)


class Castling(Move):
    def __init__(self, prev):
        super(Castling, self).__init__(prev)


class Capture(Move):
    def __init__(self, prev, new_pos):
        super(Capture, self).__init__(prev, new_pos)
