# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from enum import Enum
import operator
import random as rnd
import numpy as np
import copy


class Types(Enum):
    pawn = 1
    knight = 2
    bishop = 3
    rook = 4
    queen = 5
    king = 6
    no_piece = 7


class Move:
    def __init__(self, before):
        self.before = before
        self.captured_piece = None


class Position:

    def __init__(self, row, col):
        self.row = row
        self.col = col

        # self.occupied_by = occupied_by


class Piece:
    def __init__(self, color, type, position: Position):
        self.color = color
        self.type = type
        self.position = position

    def __str__(self):
        # print_out = [[' ' for _ in range(5)] for _ in range(5)]
        if self.type == Types.pawn:
            # return '  |  '
            return ' p'+ self.color+' '
        if self.type == Types.knight:
            # return ' /|| '
            return ' N'+ self.color+' '
        if self.type == Types.rook:
            return ' R'+self.color+' '
            # return ' ||| '
        if self.type == Types.bishop:
            return ' B'+self.color+' '
            # return ' / \\ '
        if self.type == Types.queen:
            return ' Q'+self.color+' '
            # return ' /*\\ '
        if self.type == Types.king:
            return ' K'+self.color+' '
            # return ' |*| '
        if self.type == Types.no_piece:
            return '    '
            # return '     '


class King(Piece):
    def __init__(self, color, type, position: Position):
        super().__init__(color, type, position)
        self.has_moved_once = False


def get_move(move: Move, type, is_a_capture:bool):
    new_position = move.after
    old = move.before
    old_pos_char = ''
    piece_char = ''
    capture = ''
    if type == Types.pawn and is_a_capture == True:
        old_pos_char = chr(96 + (8 - old.col))
    if type == Types.knight:
        piece_char = 'N'
    elif type == Types.bishop:
        piece_char = 'B'
    elif type == Types.rook:
        piece_char = 'R'
    elif type == Types.queen:
        piece_char = 'Q'
    elif type == Types.king:
        piece_char = 'K'
    if is_a_capture:
        capture = 'x'
    col = chr(96 + (8 - new_position.col))
    row = str(new_position.row + 1)
    return old_pos_char + piece_char + capture + col + row


class Game:
    def __init__(self, starting_pos):
        self.starting_pos = starting_pos
        self.pieces = []  # all 32 pieces and their positions
        self.board = [[Piece('_', Types.no_piece, Position(i, j)) for i in range(8)] for j in
                      range(8)]  # a 2d grid of characters representing current pieces
        self.initalize_board_and_pieces()
        self.moves = []
        self.move_names = []

    def initalize_board_and_pieces(self):

        # self.board[1][0] = Piece('w', Types.pawn, Position(1, 0))
        # self.board[1][1] = Piece('w', Types.pawn, Position(1, 1))
        # self.board[1][2] = Piece('w', Types.pawn, Position(1, 2))
        # self.board[1][3] = Piece('w', Types.pawn, Position(1, 3))
        # self.board[1][4] = Piece('w', Types.pawn, Position(1, 4))
        # self.board[1][5] = Piece('w', Types.pawn, Position(1, 5))
        # self.board[1][6] = Piece('w', Types.pawn, Position(1, 6))
        # self.board[1][7] = Piece('w', Types.pawn, Position(1, 7))

        self.board[1][0] = Piece('w', Types.no_piece, Position(1, 0))
        self.board[1][1] = Piece('w', Types.no_piece, Position(1, 1))
        self.board[1][2] = Piece('w', Types.no_piece, Position(1, 2))
        self.board[1][3] = Piece('w', Types.no_piece, Position(1, 3))
        self.board[1][4] = Piece('w', Types.no_piece, Position(1, 4))
        self.board[1][5] = Piece('w', Types.no_piece, Position(1, 5))
        self.board[1][6] = Piece('w', Types.no_piece, Position(1, 6))
        self.board[1][7] = Piece('w', Types.no_piece, Position(1, 7))

        self.board[0][0] = Piece('w', Types.rook, Position(0, 0))
        self.board[0][7] = Piece('w', Types.rook, Position(0, 7))

        # self.board[0][1] = Piece('w', Types.knight, Position(0, 1))
        # self.board[0][6] = Piece('w', Types.knight, Position(0, 6))
        # self.board[0][5] = Piece('w', Types.bishop, Position(0, 5))
        # self.board[0][2] = Piece('w', Types.bishop, Position(0, 2))

        self.board[0][1] = Piece('w', Types.no_piece, Position(0, 1))
        self.board[0][6] = Piece('w', Types.no_piece, Position(0, 6))
        self.board[0][5] = Piece('w', Types.no_piece, Position(0, 5))
        self.board[0][2] = Piece('w', Types.no_piece, Position(0, 2))

        self.board[0][3] = King('w', Types.king, Position(0, 3))
        # self.board[0][4] = Piece('w', Types.queen, Position(0, 4))

        self.board[0][4] = Piece('w', Types.no_piece, Position(0, 4))


        # self.board[6][0] = Piece('b', Types.pawn, Position(6, 0))
        # self.board[6][1] = Piece('b', Types.pawn, Position(6, 1))
        # self.board[6][2] = Piece('b', Types.pawn, Position(6, 2))
        # self.board[6][3] = Piece('b', Types.pawn, Position(6, 3))
        # self.board[6][4] = Piece('b', Types.pawn, Position(6, 4))
        # self.board[6][5] = Piece('b', Types.pawn, Position(6, 5))
        # self.board[6][6] = Piece('b', Types.pawn, Position(6, 6))
        # self.board[6][7] = Piece('b', Types.pawn, Position(6, 7))

        self.board[6][0] = Piece('b', Types.no_piece, Position(6, 0))
        self.board[6][1] = Piece('b', Types.no_piece, Position(6, 1))
        self.board[6][2] = Piece('b', Types.no_piece, Position(6, 2))
        self.board[6][3] = Piece('b', Types.no_piece, Position(6, 3))
        self.board[6][4] = Piece('b', Types.no_piece, Position(6, 4))
        self.board[6][5] = Piece('b', Types.no_piece, Position(6, 5))
        self.board[6][6] = Piece('b', Types.no_piece, Position(6, 6))
        self.board[6][7] = Piece('b', Types.no_piece, Position(6, 7))

        self.board[7][0] = Piece('b', Types.rook, Position(7, 0))
        self.board[7][7] = Piece('b', Types.rook, Position(7, 7))
        # self.board[7][1] = Piece('b', Types.knight, Position(7, 1))
        # self.board[7][6] = Piece('b', Types.knight, Position(7, 6))
        # self.board[7][5] = Piece('b', Types.bishop, Position(7, 5))
        # self.board[7][2] = Piece('b', Types.bishop, Position(7, 2))

        self.board[7][1] = Piece('b', Types.no_piece, Position(7, 1))
        self.board[7][6] = Piece('b', Types.no_piece, Position(7, 6))
        self.board[7][5] = Piece('b', Types.no_piece, Position(7, 5))
        self.board[7][2] = Piece('b',Types.no_piece, Position(7, 2))

        self.board[7][3] = King('b', Types.king, Position(7, 3))
        # self.board[7][4] = Piece('b', Types.queen, Position(7, 4))
        self.board[7][4] = Piece('b', Types.no_piece, Position(7, 4))

    def generate_moves(self, color):
        valid_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col].type != Types.no_piece and self.board[row][col].color == color:
                    valid_moves.extend(self.get_valid_moves(self.board[row][col]))
        return valid_moves

    def get_valid_moves(self, square):
        valid_moves = []
        if square.type == Types.pawn:
            moves = self.get_pawn_moves(square)
            if len(moves) > 0:
                valid_moves.extend(moves)
        if square.type == Types.bishop:
            moves = self.get_bishop_moves(square)
            if len(moves) > 0:
                valid_moves.extend(moves)
        if square.type == Types.knight:
            moves = self.get_knight_moves(square)
            if len(moves) > 0:
                valid_moves.extend(moves)
        if square.type == Types.rook:
            moves = self.get_rook_moves(square)
            if len(moves) > 0:
                valid_moves.extend(moves)
        if square.type == Types.queen:
            moves = self.get_queen_moves(square)
            if len(moves) > 0:
                valid_moves.extend(moves)
        if square.type == Types.king:
            moves = self.get_king_moves(square)
            if len(moves) > 0:
                valid_moves.extend(moves)
        return valid_moves

    def update_board(self, move: Move):
        is_a_capture = False
        new_position = move.after
        old_position = move.before
        if self.board[new_position.row][new_position.col].type != Types.no_piece:
            is_a_capture = True




        captured_position = move.captured_piece
        old = copy.copy(self.board[old_position.row][old_position.col])
        new = copy.copy(self.board[new_position.row][new_position.col])
        self.board[new_position.row][new_position.col] = old
        if self.board[new_position.row][new_position.col].type == Types.king:
            self.board[new_position.row][new_position.col].has_moved_once = True

        # update old position with blank since piece is leaving the square
        self.board[old_position.row][old_position.col].type = Types.no_piece
        self.board[old_position.row][old_position.col].color = '_'
        self.board[old_position.row][old_position.col].position = old_position


        if captured_position is not None:
            # update captured position with blank (comes into play for en passant)
            self.board[captured_position.row][captured_position.col].type = Types.no_piece
            self.board[captured_position.row][captured_position.col].color = '_'
            self.board[captured_position.row][captured_position.col].position = captured_position
            is_a_capture = True


        self.board[new_position.row][new_position.col].position = new_position
        self.move_names.append(get_move(move, self.board[new_position.row][new_position.col].type, is_a_capture))
        self.moves.append(move)


        # short castling
        if self.board[new_position.row][new_position.col].type == Types.king and new_position.col == old_position.col-2:
            self.board[new_position.row][2].type = Types.rook
            self.board[new_position.row][2].color = self.board[new_position.row][new_position.col].color
            self.board[new_position.row][0].type = Types.no_piece
            self.board[new_position.row][0].color = '_'
            self.board[new_position.row][new_position.col].has_moved_once = True


        # long castling

        elif self.board[new_position.row][new_position.col].type == Types.king and new_position.col == old_position.col + 2:
            self.board[new_position.row][4].type = Types.rook
            self.board[new_position.row][4].color = self.board[new_position.row][new_position.col].color
            self.board[new_position.row][7].type = Types.no_piece
            self.board[new_position.row][7].color = '_'
            self.board[new_position.row][new_position.col].has_moved_once = True

    def get_pawn_moves(self, square):
        valid_moves = []
        blocked = 0
        # white moves forward
        if square.color == 'w':
            op = operator.add
        else:

            # black moves in opposite direction of white
            op = operator.sub

        # one step forward move
        current_square = square.position
        move1 = Move(current_square)
        position1 = Position(op(current_square.row, 1), current_square.col)
        if self.board[op(current_square.row, 1)][current_square.col].type != Types.no_piece:
            blocked = 1
        else:
            move1.after = position1
            valid_moves.append(move1)

        # two steps forward move for white
        if not blocked and square.color == 'w' and square.position.row == 1:
            if self.board[current_square.row+2][current_square.col].type == Types.no_piece:
                move2 = Move(current_square)
                position2 = Position(current_square.row + 2, current_square.col)
                move2.after = position2
                valid_moves.append(move2)

        if not blocked and square.color == 'b' and square.position.row == 6:
            if self.board[current_square.row-2][current_square.col].type == Types.no_piece:
                move2 = Move(current_square)
                position2 = Position(current_square.row - 2, current_square.col)
                move2.after = position2
                valid_moves.append(move2)

        # check if opposing piece is at diagonal square
        move1 = Move(current_square)
        move2 = Move(current_square)
        position1 = Position(op(current_square.row, 1), current_square.col + 1)
        position2 = Position(op(current_square.row, 1), current_square.col - 1)

        if position1.col < 8 and self.board[position1.row][position1.col].color != square.color and \
                self.board[position1.row][position1.col].type != Types.no_piece:
            move1.after = position1
            valid_moves.append(move1)
        if position2.col >= 0 and self.board[position2.row][position2.col].color != square.color \
                and self.board[position2.row][position2.col].type != Types.no_piece:
            move2.after = position2
            valid_moves.append(move2)


        # en passant for white on upper left diagonal
        move3 = Move(current_square)
        prev_mov = None
        if len(self.moves) > 0:
            prev_mov = self.moves[-1]
        if prev_mov is not None:
            if square.color == 'w':
                if current_square.col-1 >= 0 and self.board[current_square.row][current_square.col-1].type == Types.pawn and self.board[current_square.row][current_square.col-1].color != square.color and prev_mov.before.row == current_square.row + 2 and prev_mov.after.row == current_square.row:
                    move3.after = Position(current_square.row+1, current_square.col-1)
                    valid_moves.append(move3)
                elif current_square.col+1 <= 7 and self.board[current_square.row][current_square.col+1].type == Types.pawn and self.board[square.position.row][square.position.col+1].color != square.color and prev_mov.before.row == square.position.row + 2 and prev_mov.after.row == square.position.row:
                    move3.after = Position(square.position.row + 1, square.position.col + 1)
                    valid_moves.append(move3)
            elif square.color == 'b':
                if current_square.col-1 >= 0 and self.board[square.position.row][square.position.col-1].type == Types.pawn and self.board[square.position.row][square.position.col-1].color != square.color and prev_mov.before.row == square.position.row - 2 and prev_mov.after.row == square.position.row:
                    move3.after = Position(square.position.row-1, square.position.col-1)
                    valid_moves.append(move3)
                elif current_square.col+1 <= 7 and self.board[square.position.row][square.position.col+1].type == Types.pawn and self.board[square.position.row][square.position.col+1].color != square.color and prev_mov.before.row == square.position.row - 2 and prev_mov.after.row == square.position.row:
                    move3.after = Position(square.position.row - 1, square.position.col + 1)
                    valid_moves.append(move3)

        return valid_moves

    def get_bishop_moves(self, square):
        valid_moves = []
        row = square.position.row
        col = square.position.col
        # upper left diagonal

        i = 1
        while row + i <= 7 and col + i <= 7:
            if not self.board[row + i][col + i].type == Types.no_piece:
                if self.board[row + i][col + i].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row + i, col + i)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row + i, col + i)
            valid_moves.append(move)
            i += 1

        # upper right diagonal
        i = 1
        while row + i <= 7 and col - i >= 0:
            if not self.board[row + i][col - i].type == Types.no_piece:
                if self.board[row + i][col - i].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row + i, col - i)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row + i, col - i)
            valid_moves.append(move)
            i += 1

        # lower left diagonal
        i = 1
        while row - i >= 0 and col - i >= 0:
            if not self.board[row - i][col - i].type == Types.no_piece:
                if self.board[row - i][col - i].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row - i, col - i)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row - i, col - i)
            valid_moves.append(move)
            i += 1
        # lower right diagonal
        i = 1
        while row - i >= 0 and col + i <= 7:
            if not self.board[row - i][col + i].type == Types.no_piece:
                if self.board[row - i][col + i].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row - i, col + i)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row - i, col + i)
            valid_moves.append(move)
            i += 1
        return valid_moves

    def get_knight_moves(self, square):
        valid_moves = []
        row = square.position.row
        col = square.position.col
        # upper left diagonal
        move = Move(square.position)
        if row - 1 >= 0 and col - 2 >= 0 and self.board[row - 1][col - 2].color != square.color:
            position1 = Position(row - 1, col - 2)
            move.after = position1
            valid_moves.append(move)
        move = Move(square.position)
        if row + 1 < 8 and col - 2 >= 0 and self.board[row + 1][col - 2].color != square.color:
            position1 = Position(row + 1, col - 2)
            move.after = position1
            valid_moves.append(move)
        move = Move(square.position)
        if row + 2 < 8 and col - 1 >= 0 and self.board[row + 2][col - 1].color != square.color:
            position1 = Position(row + 2, col - 1)
            move.after = position1
            valid_moves.append(move)
        move = Move(square.position)
        if row - 2 >= 0 and col - 1 >= 0 and self.board[row - 2][col - 1].color != square.color:
            position1 = Position(row - 2, col - 1)
            move.after = position1
            valid_moves.append(move)
        move = Move(square.position)
        if row + 2 <= 7 and col + 1 <= 7 and self.board[row + 2][col + 1].color != square.color:
            position1 = Position(row + 2, col + 1)
            move.after = position1
            valid_moves.append(move)
        move = Move(square.position)
        if row - 2 >= 0 and col + 1 <= 7 and self.board[row - 2][col + 1].color != square.color:
            position1 = Position(row - 2, col + 1)
            move.after = position1
            valid_moves.append(move)
        move = Move(square.position)
        if row - 1 >= 0 and col + 2 <= 7 and self.board[row - 1][col + 2].color != square.color:
            position1 = Position(row - 1, col + 2)
            move.after = position1
            valid_moves.append(move)
        move = Move(square.position)
        if row + 1 <= 7 and col + 2 <= 7 and self.board[row + 1][col + 2].color != square.color:
            position1 = Position(row + 1, col + 2)
            move.after = position1
            valid_moves.append(move)
        return valid_moves

    def get_rook_moves(self, square):
        valid_moves = []
        row = square.position.row
        col = square.position.col
        i = 1
        while row + i <= 7:
            if not self.board[row + i][col].type == Types.no_piece:
                if self.board[row + i][col].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row + i, col)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row + i, col)
            valid_moves.append(move)
            i += 1
        i = 1
        while row - i >= 0:
            if not self.board[row - i][col].type == Types.no_piece:
                if self.board[row - i][col].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row - i, col)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row - i, col)
            valid_moves.append(move)
            i += 1
        i = 1
        while col - i >= 0:
            if not self.board[row][col - i].type == Types.no_piece:
                if self.board[row][col - i].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row + i, col)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row, col - i)
            valid_moves.append(move)
            i += 1
        i = 1
        while col + i <= 7:
            if not self.board[row][col + i].type == Types.no_piece:
                if self.board[row][col + i].color == square.color:
                    break
                else:
                    move = Move(square.position)
                    move.after = Position(row, col + i)
                    valid_moves.append(move)
                    break
            move = Move(square.position)
            move.after = Position(row, col + i)
            valid_moves.append(move)
            i += 1
        return valid_moves

    def get_queen_moves(self, square):
        valid_moves = []
        valid_moves.extend(self.get_rook_moves(square))
        valid_moves.extend(self.get_bishop_moves(square))
        return valid_moves

    def get_king_moves(self, square):
        valid_moves = []
        castling = True
        long_castling = True
        row = square.position.row
        col = square.position.col

        # checking if castling is possible
        if square.has_moved_once == False:
            i = 1
            while self.board[row][col - i].type != Types.rook:
                if self.board[row][col-i].type != Types.no_piece:
                    castling = False
                    break
                i+=1
            if castling:
                move = Move(square.position)
                move.after = Position(row, col-2)
                valid_moves.append(move)

        # checking if long castling is possible
        if square.has_moved_once == False:
            i = 1
            while self.board[row][col + i].type != Types.rook:
                if self.board[row][col+ i].type != Types.no_piece:
                    long_castling = False
                    break
                i+=1
            if long_castling:
                move = Move(square.position)
                move.after = Position(row, col+2)
                valid_moves.append(move)


        # upper left diagonal
        if row + 1 <= 7 and col + 1 <= 7 and self.board[row + 1][col + 1].color != square.color:
            move1 = Move(square.position)
            move1.after = Position(row + 1, col + 1)
            valid_moves.append(move1)

        # upper right diagonal
        if row + 1 <= 7 and col - 1 >= 0 and self.board[row + 1][col - 1].color != square.color:
            move2 = Move(square.position)
            move2.after = Position(row + 1, col - 1)
            valid_moves.append(move2)

        # lower left diagonal
        if row - 1 >= 0 and col - 1 >= 0 and self.board[row - 1][col - 1].color != square.color:
            move3 = Move(square.position)
            move3.after = Position(row - 1, col - 1)
            valid_moves.append(move3)

        # lower right diagonal
        if row - 1 >= 0 and col + 1 <= 7 and self.board[row - 1][col + 1].color != square.color:
            move4 = Move(square.position)
            move4.after = Position(row - 1, col + 1)
            valid_moves.append(move4)

        if row + 1 <= 7 and self.board[row + 1][col].color != square.color:
            move5 = Move(square.position)
            move5.after = Position(row + 1, col)
            valid_moves.append(move5)

        if col + 1 <= 7 and self.board[row][col + 1].color != square.color:
            move6 = Move(square.position)
            move6.after = Position(row, col + 1)
            valid_moves.append(move6)

        if row - 1 >= 0 and self.board[row - 1][col].color != square.color:
            move7 = Move(square.position)
            move7.after = Position(row - 1, col)
            valid_moves.append(move7)

        if col - 1 >= 0 and self.board[row][col - 1].color != square.color:
            move8 = Move(square.position)
            move8.after = Position(row, col - 1)
            valid_moves.append(move8)

        return valid_moves


def print_chess_board(board):
    for i in range(len(board)):
        print('\n')
        for j in range(len(board[0])):
            print(board[i][j], end='\t')


def print_blank():
    print('     ')
    print('     ')
    print('     ')
    print('     ')
    print('     ')


def print_bishop():
    print(' / \\ ')
    print(' \|/ ')
    print(' --- ')
    print('  |  ')
    print(' --- ')


def print_knight():
    print('/^|')
    print(' ||')
    print('---')
    print(' ||')
    print(' ||')
    print('---')


def print_pawn():
    print(' | ')
    print(' | ')
    print('---')
    print(' | ')
    print(' | ')
    print('---')


def print_rook():
    print(' ||| ')
    print(' ||| ')
    print(' ||| ')
    print(' ||| ')
    print(' ___ ')


def print_queen():
    print(' ||| ')
    print(' /|\\ ')
    print(' \\|/ ')
    print(' ||| ')
    print(' ___ ')


def print_king():
    print(' /-\\ ')
    print(' ||| ')
    print(' --- ')
    print(' ||| ')
    print(' ___ ')


if __name__ == '__main__':

    turn = 'w'
    starting_pos = [('e4', 'e5')]
    game = Game(starting_pos)
    while 1:
        moves = game.generate_moves(turn)
        if len(moves) == 0:
            print('\n---game over---')
            break
        chosen_move = rnd.choice(moves)
        game.update_board(chosen_move)
        print(f'\nmove - {game.move_names[-1]}\n')
        if turn == 'w':
            turn = 'b'
        else:
            turn = 'w'
        print_chess_board(game.board)
        print('\n')
        print('-' * 100)

    print(moves)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
