from collections import defaultdict

from Piece import Piece, Pawn, Rook, Bishop, Knight, King, Queen
import itertools


class Board:
    def __init__(self, board_dim):
        self.turn = 'white'
        self.white_pos = initialize_white_pos()
        self.black_pos = initalize_black_pos()
        self.own_pieces = self.white_pos.keys()
        self.oppos_pieces = self.black_pos.keys()
        self.en_passant_pos = None
        self.diagonals = generate_diagonals(board_dim)
        self.rows = get_rows(board_dim)
        self.columns = get_columns(board_dim)
        self.not_moved_pieces = set(self.white_pos.keys()+self.black_pos.keys())
        self.turn = 'white'
        self.own_pieces = self.white_pos
        self.oppos_pieces = self.black_pos
        self.white_moves = defaultdict(list)
        self.black_moves = defaultdict(list)
        for pos, piece in self.white_pos.items():
            self.white_moves[pos] = self.get_moves(pos, piece)
        self.update_turn()
        for pos, piece in self.black_pos.items():
            self.black_moves[pos] = self.get_moves(pos, piece)

    def update_not_moved_pieces(self, pos):
        self.not_moved_pieces.remove(pos)

    def update_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

        if self.turn == 'white':
            self.own_pieces = self.white_pos.keys()
            self.oppos_pieces = self.black_pos.keys()
        else:
            self.own_pieces = self.black_pos.keys()
            self.oppos_pieces = self.white_pos.keys()


    def get_moves(self, pos, piece):
        if piece == 'Pawn':
            return self.get_pawn_moves(pos)
        elif piece == 'Rook':
            return self.get_rook_moves(pos)
        elif piece == 'Bishop':
            return self.get_bishop_moves(pos)
        elif piece == 'Queen':
            return self.get_bishop_moves(pos) + self.get_rook_moves(pos)
        elif piece == 'King':
            return self.get_king_moves(pos)
        elif piece == 'Knight':
            return self.get_knight_moves(pos)

    def get_pawn_moves(self, pos):
        moves = []

        if self.turn == 'white':
            moves.append(self.get_white_pawn_moves(pos))
        else:
            moves.append(self.get_black_pawn_moves(pos))
        return moves

    def get_white_pawn_moves(self, pos):
        moves = []
        row = pos[0]
        col = pos[1]
        if (row + 1, col) not in self.white_pos.keys() and (row + 1, col) not in self.black_pos.keys():
            moves.append((row + 1, col))
        if (row + 1, col + 1) in self.black_pos.keys():
            moves.append((row + 1, col + 1))
        if (row + 1, col - 1) in self.black_pos.keys():
            moves.append((row + 1, col - 1))

        # for white, if pawn is on 2nd row
        if row == 1:
            if (row + 2, col) not in self.white_pos.keys() and (row + 2, col) not in self.black_pos.keys():
                moves.append((row + 2, col))

        if self.en_passant_pos is not None:
            if self.en_passant_pos[0] == row and self.en_passant_pos[1] == col + 1:
                moves.append((row + 1, col + 1))
            elif self.en_passant_pos[0] == row and self.en_passant_pos[1] == col - 1:
                moves.append((row + 1, col - 1))

        return moves

    def get_black_pawn_moves(self, pos):
        moves = []
        row = pos[0]
        col = pos[1]
        if (row - 1, col) not in self.white_pos.keys() and (row - 1, col) not in self.black_pos.keys():
            moves.append((row - 1, col))
        if (row - 1, col + 1) in self.black_pos.keys():
            moves.append((row - 1, col + 1))
        if (row - 1, col - 1) in self.black_pos.keys():
            moves.append((row - 1, col - 1))

        # for white, if pawn is on 2nd row
        if row == 6:
            if (row - 2, col) not in self.white_pos.keys() and (row - 2, col) not in self.black_pos.keys():
                moves.append((row - 2, col))

        if self.en_passant_pos is not None:
            if self.en_passant_pos[0] == row and self.en_passant_pos[1] == col + 1:
                moves.append((row - 1, col + 1))
            elif self.en_passant_pos[0] == row and self.en_passant_pos[1] == col - 1:
                moves.append((row - 1, col - 1))

        return moves

    def get_rook_moves(self, pos):
        row = None
        col = None
        moves = []
        # for set in self.rows:
        #     if pos in set:
        #         row = sorted(list(set), key=lambda t:(t[0], t[1]))
        #         break
        # for set in self.columns:
        #     if pos in set:
        #         col = sorted(list(set), key=lambda t:(t[0], t[1]))
        #         break
        # if row is None or col is None:
        #     return []

        cr =pos[0]
        cc =pos[1]
        while 0 <= cr+1 < 8 and 0 <= cc < 8 and (cr+1, cc) not in self.own_pieces:
            moves.append((cr+1, cc))
            if (cr+1, cc) in self.oppos_pieces:
                break
            cr += 1

        cr = pos[0]
        cc = pos[1]
        while 0 <= cr - 1 < 8 and 0 <= cc < 8 and (cr - 1, cc) not in self.own_pieces:
            moves.append((cr - 1, cc))
            if (cr - 1, cc) in self.oppos_pieces:
                break
            cr -= 1

        cr = pos[0]
        cc = pos[1]
        while 0 <= cr < 8 and 0 <= cc+1 < 8 and (cr, cc+1) not in self.own_pieces:
            moves.append((cr, cc+1))
            if (cr, cc+1) in self.oppos_pieces:
                break
            cc += 1

        cr = pos[0]
        cc = pos[1]
        while 0 <= cr < 8 and 0 <= cc - 1 < 8 and (cr, cc - 1) not in self.own_pieces:
            moves.append((cr, cc - 1))
            if (cr, cc - 1) in self.oppos_pieces:
                break
            cr -= 1

        return moves

    def get_bishop_moves(self, pos):
        moves = []
        cr = pos[0]
        cc = pos[1]
        while 0 <= cr + 1 < 8 and 0 <= cc+1 < 8 and (cr + 1, cc+1) not in self.own_pieces:
            moves.append((cr + 1, cc+1))
            if (cr + 1, cc+1) in self.oppos_pieces:
                break
            cr += 1
            cc += 1

        cr = pos[0]
        cc = pos[1]
        while 0 <= cr - 1 < 8 and 0 <= cc+1 < 8 and (cr - 1, cc+1) not in self.own_pieces:
            moves.append((cr - 1, cc+1))
            if (cr - 1, cc+1) in self.oppos_pieces:
                break
            cr -= 1
            cc += 1

        cr = pos[0]
        cc = pos[1]
        while 0 <= cr - 1 < 8 and 0 <= cc - 1 < 8 and (cr - 1, cc - 1) not in self.own_pieces:
            moves.append((cr - 1, cc - 1))
            if (cr - 1, cc - 1) in self.oppos_pieces:
                break
            cc -= 1
            cr -= 1

        cr = pos[0]
        cc = pos[1]
        while 0 <= cr + 1 < 8 and 0 <= cc - 1 < 8 and (cr, cc - 1) not in self.own_pieces:
            moves.append((cr+1, cc - 1))
            if (cr + 1, cc - 1) in self.oppos_pieces:
                break
            cr += 1
            cc -= 1

        return moves

    def get_king_moves(self, pos):
        row, col = pos
        moves = [(row+i, col+j) for i, j in itertools.product([0, 1, -1],repeat=2)]
        moves = [(row, col) for row, col in moves if (row, col) !=(pos[0],pos[1]) and 0 <= row < 8 and 0 <= col < 8 and (row, col) not in self.own_pieces]
        return moves

    def get_knight_moves(self, pos):
        row = pos[0]
        col = pos[1]
        a = [-2, 2]
        b = [-1, 1]
        moves_1 = [(row + i, col + j) for i, j in itertools.product(a, b)]
        moves_1 = [(row,col) for row, col in moves_1 if 0 <= row < 8 and 0 <= col < 8 and (row, col) not in
                   self.own_pieces]
        a = [-1, 1]
        b = [-2, 2]
        moves_2 = [(row + i, col + j) for i, j in itertools.product(a, b)]
        moves_2 = [(row, col) for row, col in moves_2 if 0 <= row < 8 and 0 <= col < 8 and (row, col) not in
                   self.own_pieces]
        return moves_1 + moves_2

    def add_move(self, piece, move):
        pass


def generate_diagonals(board_dim):
    rows, cols = board_dim[0], board_dim[1]
    diagonals = []
    for col in range(cols):
        init_row = -1
        init_col = col - 1
        diagonal_set = set()
        while 0 <= init_row + 1 < board_dim[0] and 0 <= init_col + 1 < board_dim[1]:
            diagonal_set.add((init_row + 1, init_col + 1))
            init_row += 1
            init_col += 1
        if len(diagonal_set) > 0:
            diagonals.append(diagonal_set)
    for row in range(rows):
        init_row = row
        init_col = -1
        diagonal_set = set()
        while 0 <= init_row + 1 < board_dim[0] and 0 <= init_col + 1 < board_dim[1]:
            diagonal_set.add((init_row + 1, init_col + 1))
            init_row += 1
            init_col += 1
        if len(diagonal_set) > 0:
            diagonals.append(diagonal_set)
    for row in range(rows):
        init_row = row
        init_col = board_dim[1]
        diagonal_set = set()
        while 0 <= init_row + 1 < board_dim[0] and 0 <= init_col - 1 < board_dim[1]:
            diagonal_set.add((init_row + 1, init_col - 1))
            init_row += 1
            init_col -= 1
        if len(diagonal_set) > 0:
            diagonals.append(diagonal_set)
    for col in range(cols, 0, -1):
        init_row = -1
        init_col = col
        diagonal_set = set()
        while 0 <= init_row + 1 < board_dim[0] and 0 <= init_col - 1 < board_dim[1]:
            diagonal_set.add((init_row + 1, init_col - 1))
            init_row += 1
            init_col -= 1
        if len(diagonal_set) > 0:
            diagonals.append(diagonal_set)

    return diagonals


def get_rows(param):
    '''
    The squares on the board for each row
    '''
    rows = param[0]
    cols = param[1]
    straights = []
    for row in range(rows):
        row_set = set()
        col = 0

        while 0 <= col < cols:
            row_set.add((row, col))
            col += 1
        straights.append(row_set)
    return straights


def get_columns(param):
    '''
    the squares on the board for each column
    '''
    rows = param[0]
    cols = param[1]
    straights = []
    for col in range(cols):
        row_set = set()
        row = 0

        while 0 <= row < rows:
            row_set.add((row, col))
            row += 1
        straights.append(row_set)

    return straights


def initialize_white_pos():
    '''
    The white pieces, placed at correct locations as per typical configuration in normal chess
    '''
    white_pos = {}
    white_pos[(0, 0)] = 'Rook'
    white_pos[(0, 1)] = 'Knight'
    white_pos[(0, 2)] = 'Bishop'
    white_pos[(0, 3)] = 'King'
    white_pos[(0, 4)] = 'Queen'
    white_pos[(0, 5)] = 'Bishop'
    white_pos[(0, 6)] = 'Knight'
    white_pos[(0, 7)] = 'Rook'
    white_pos[(1, 0)] = 'Pawn'
    white_pos[(1, 1)] = 'Pawn'
    white_pos[(1, 2)] = 'Pawn'
    white_pos[(1, 3)] = 'Pawn'
    white_pos[(1, 4)] = 'Pawn'
    white_pos[(1, 5)] = 'Pawn'
    white_pos[(1, 6)] = 'Pawn'
    white_pos[(1, 7)] = 'Pawn'
    return white_pos


def initalize_black_pos():
    '''
    The black pieces, placed at correct locations 
    '''
    black_pos = {}
    black_pos[(7, 0)] = 'Rook'
    black_pos[(7, 1)] = 'Knight'
    black_pos[(7, 2)] = 'Bishop'
    black_pos[(7, 3)] = 'King'
    black_pos[(7, 4)] = 'Queen'
    black_pos[(7, 5)] = 'Bishop'
    black_pos[(7, 6)] = 'Knight'
    black_pos[(7, 7)] = 'Rook'
    black_pos[(6, 0)] = 'Pawn'
    black_pos[(6, 1)] = 'Pawn'
    black_pos[(6, 2)] = 'Pawn'
    black_pos[(6, 3)] = 'Pawn'
    black_pos[(6, 4)] = 'Pawn'
    black_pos[(6, 5)] = 'Pawn'
    black_pos[(6, 6)] = 'Pawn'
    black_pos[(6, 7)] = 'Pawn'
    return black_pos


def generate_moves(white_pos):
    white_moves = {}
    for pos, piece in white_pos.items():
        white_moves[pos] = get_moves(pos, piece)
