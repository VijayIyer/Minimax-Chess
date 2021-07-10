import copy


from Colors import Colors
import operator


class Position:
    def __init__(self, pos):
        self.row = pos[0]
        self.col = pos[1]


class Move:
    def __init__(self, prev, new_pos):
        self.prev = prev
        self.new_pos = new_pos

    def __str__(self):
        col = chr(96 + (8 - self.new_pos.col))
        row = str(self.new_pos.row + 1)
        return col + row


class En_passant(Move):
    def __init__(self, prev, new_pos):
        super(En_passant, self).__init__(prev, new_pos)



    def __str__(self):
        col = chr(96 + (8 - self.new_pos.col))
        row = str(self.new_pos.row + 1)

        return 'x' + col + row


class Castling(Move):
    def __init__(self, prev, new_pos):
        super(Castling, self).__init__(prev, new_pos)

    def __str__(self):
        if self.prev.col == self.new_pos.col +2:
            return 'O-O'
        else:
            return 'O-O-O'


class Capture(Move):
    def __init__(self, prev, new_pos):
        super(Capture, self).__init__(prev, new_pos)

    def __str__(self):
        col = chr(96 + (8 - self.new_pos.col))
        row = str(self.new_pos.row + 1)
        return 'x' + col + row