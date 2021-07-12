# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from enum import Enum
import operator
import random as rnd
import numpy as np
import copy
import time
import Colors
from Colors import Colors
import Piece
import itertools
from Piece import Piece, Pawn, Queen, Knight, King, Bishop, Rook
from Moves import Position, Move, En_passant, Capture, Castling
import re


def find_piece_rows(piece_type, board, color):
    candidate_rows = []
    candidate_cols = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if type(board[i][j]) == piece_type and board[i][j].color == color:
                candidate_rows.append(i)
                candidate_cols.append(j)

    return candidate_rows, candidate_cols


class Game:
    def __init__(self, starting_pos):

        self.starting_pos = starting_pos
        self.board = self.initalize_board_and_pieces()
        self.moves = []
        self.move_names = []
        self.turn = Colors.white
        self.move_count = 1
        self.game_moves_total = ''
        if len(starting_pos) > 0:
            for move_name in starting_pos:

                move = self.infer_move(move_name, self.turn)
                self.update_board(move)
                if self.turn == Colors.white:
                    self.turn = Colors.black
                    self.game_moves_total += ' ' + str(self.move_count) + '.'
                    self.game_moves_total += self.move_names[-1]
                elif self.turn == Colors.black:
                    self.turn = Colors.white

                    self.game_moves_total += ' ' + self.move_names[-1]
                    self.move_count += 1

    def initalize_board_and_pieces(self):
        board = [[Piece(color=Colors.blank) for _ in range(8)] for _ in range(8)]
        board[1][0] = Pawn(color=Colors.white)
        board[1][1] = Pawn(color=Colors.white)
        board[1][2] = Pawn(color=Colors.white)
        board[1][3] = Pawn(color=Colors.white)
        board[1][4] = Pawn(color=Colors.white)
        board[1][5] = Pawn(color=Colors.white)
        board[1][6] = Pawn(color=Colors.white)
        board[1][7] = Pawn(color=Colors.white)
        board[0][0] = Rook(color=Colors.white)
        board[0][7] = Rook(color=Colors.white)

        board[0][1] = Knight(color=Colors.white)
        board[0][6] = Knight(color=Colors.white)
        board[0][5] = Bishop(color=Colors.white)
        board[0][2] = Bishop(color=Colors.white)
        board[0][3] = King(color=Colors.white)

        board[0][4] = Queen(color=Colors.white)

        board[6][0] = Pawn(color=Colors.black)
        board[6][1] = Pawn(color=Colors.black)
        board[6][2] = Pawn(color=Colors.black)
        board[6][3] = Pawn(color=Colors.black)
        board[6][4] = Pawn(color=Colors.black)
        board[6][5] = Pawn(color=Colors.black)
        board[6][6] = Pawn(color=Colors.black)
        board[6][7] = Pawn(color=Colors.black)
        board[7][0] = Rook(color=Colors.black)
        board[7][7] = Rook(color=Colors.black)

        board[7][1] = Knight(color=Colors.black)
        board[7][6] = Knight(color=Colors.black)
        board[7][5] = Bishop(color=Colors.black)
        board[7][2] = Bishop(color=Colors.black)
        board[7][3] = King(color=Colors.black)
        board[7][4] = Queen(color=Colors.black)
        return board

    def generate_moves(self, color):
        valid_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col].color == color:
                    piece = self.board[row][col]
                    valid_moves.extend(piece.get_moves(Position((row, col)), self))
        return valid_moves

    def update_board(self, chosen_move):
        self.board = self.act_on_move(chosen_move)
        self.moves.append(chosen_move)
        self.is_in_check = ''
        if Piece.is_in_check(self.board, game.turn, Piece.get_king_pos(self.board, game.turn)):
            self.is_in_check = '+'
        self.move_names.append(str(self.board[chosen_move.new_pos.row][chosen_move.new_pos.col]) + str(chosen_move))

    def act_on_move(self, move: Move):
        if type(move) == Castling:

            # updating king position
            new_board = copy.deepcopy(self.board)
            new_row, new_col = move.new_pos.row, move.new_pos.col
            old_row, old_col = move.prev.row, move.prev.col
            new_board[new_row][new_col] = copy.deepcopy(self.board[old_row][old_col])
            new_board[old_row][old_col] = Piece(color=Colors.blank)
            new_board[new_row][new_col].has_moved = True

            # updating rook position
            if new_col == old_col - 2:
                new_board[new_row][new_col + 1] = copy.deepcopy(new_board[new_row][0])
                new_board[new_row][new_col + 1].has_moved = True
                new_board[new_row][0] = Piece(color=Colors.blank)
            else:
                new_board[new_row][new_col - 1] = copy.deepcopy(new_board[new_row][7])
                new_board[new_row][new_col - 1].has_moved = True
                new_board[new_row][7] = Piece(color=Colors.blank)

            return new_board

        elif type(move) == En_passant:
            op = operator.sub if self.board[move.prev.row][move.prev.col].color == Colors.white else operator.add
            new_board = copy.deepcopy(self.board)
            new_row, new_col = move.new_pos.row, move.new_pos.col
            old_row, old_col = move.prev.row, move.prev.col
            new_board[new_row][new_col] = copy.deepcopy(self.board[old_row][old_col])
            new_board[old_row][old_col] = Piece(color=Colors.blank)
            new_board[new_row][new_col].has_moved = True
            # updating captured piece
            new_board[op(new_row, 1)][new_col] = Piece(color=Colors.blank)
            return new_board
        else:
            new_board = copy.deepcopy(self.board)
            new_row, new_col = move.new_pos.row, move.new_pos.col
            old_row, old_col = move.prev.row, move.prev.col
            new_board[new_row][new_col] = copy.deepcopy(self.board[old_row][old_col])
            new_board[old_row][old_col] = Piece(color=Colors.blank)
            new_board[new_row][new_col].has_moved = True
            return new_board

    def infer_move(self, move, color):
        '''
        work on this regex
        (?'piece'[K|N|B|R|Q]?)(?'amb'[a-h1-8]?)(?'capture'[x]?)(?'newcol'[a-h]{1})(?'newrow'[1-8]{1})(?'checkormate'[+|#]*)$

        :param move:
        :param color:
        :return:
        '''
        pattern = re.compile('(?P<piece>[K|N|B|R|Q]?)(?P<amb>[a-h1-8]?)(?P<capture>[x]?)(?P<newcol>[a-h]{1})('
                             '?P<newrow>[1-8]{1})(?P<checkormate>[+|#]*)$|(?P<LongCastle>^(O-O-O){1})$|(?P<Castle>^('
                             'O-O){1})$')
        m = re.match(pattern=pattern, string=move)
        m_dict = m.groupdict()
        piece_type = Pawn
        if m_dict['LongCastle'] is not None:
            if color == Colors.white:
                return Castling(Position((0, 3)), Position((0, 5)))
            elif color == Colors.black:
                return Castling(Position((7, 3)), Position((7, 5)))
        if m_dict['Castle'] is not None:
            if color == Colors.white:
                return Castling(Position((0, 3)), Position((0, 1)))
            elif color == Colors.black:
                return Castling(Position((7, 3)), Position((7, 1)))

        if m_dict['piece'] == '':
            piece_type = Pawn
        elif m_dict['piece'] == 'N':
            piece_type = Knight
        elif m_dict['piece'] == 'B':
            piece_type = Bishop
        elif m_dict['piece'] == 'R':
            piece_type = Rook
        elif m_dict['piece'] == 'Q':
            piece_type = Queen
        elif m_dict['piece'] == 'K':
            piece_type = King

        old_row, old_col = 0, 0
        if m_dict['amb'] != '':
            old_col = 104 - ord(m_dict['amb'])

        if m_dict['capture'] != '':
            move_type = Capture
        else:
            move_type = Move

        new_row, new_col = int(m_dict['newrow']) - 1, 104 - ord(m_dict['newcol'])

        candidate_rows, candidate_cols = find_piece_rows(piece_type, self.board, color)
        candidate_moves = []
        for row, col in zip(candidate_rows, candidate_cols):
            candidate_moves.extend(self.board[row][col].get_moves(Position((row, col)), self))

        if len(candidate_moves) == 0:
            return []
        for move in candidate_moves:
            if type(move) == En_passant and move_type == Capture:
                move_type = En_passant
            if move.new_pos.row == new_row and move.new_pos.col == new_col:
                return move_type(move.prev, move.new_pos)
        return []


def print_chess_board(board):
    for i in range(len(board)):
        print('\n')
        for j in range(len(board[0])):
            print(board[i][j], end='')
            print(board[i][j].color, end='\t')


def print_dots(number_of_dots):
    print('\r' + '*' * number_of_dots, end='')
    time.sleep(1)


if __name__ == '__main__':
    # num = 1
    # while 1:
    #     print_dots(number_of_dots=num)
    #     num += 1
    #     if num > 10:
    #         num = 1

    starting_pos = ['e4', 'e5', 'Bc4', 'Nc6', 'Qf3', 'Bc5', 'Qxf7#']
    game = Game(starting_pos)

    while 1:

        moves = game.generate_moves(game.turn)
        if len(moves) == 0:
            game.is_in_check = '#'
            print('\n---game over---')
            break
        chosen_move = rnd.choice(moves)
        game.update_board(chosen_move)

        if game.turn == Colors.white:
            game.turn = Colors.black
            game.game_moves_total += ' ' + str(game.move_count) + '.'
            game.game_moves_total += game.move_names[-1]+game.is_in_check
            print(game.game_moves_total)
        else:
            game.turn = Colors.white
            game.game_moves_total += ' ' + game.move_names[-1]+game.is_in_check
            print(game.game_moves_total)
            game.move_count += 1

        print_chess_board(game.board)
        print('\n')
        print('-' * 100)

    print(game.game_moves_total)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
