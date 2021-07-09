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
from Piece import Piece, Pawn, Queen, Knight, King, Bishop, Rook
from Moves import Position, Move, En_passant, Capture, Castling


class Game:
    def __init__(self, starting_pos):

        self.starting_pos = starting_pos
        self.board = self.initalize_board_and_pieces()
        self.moves = []
        self.move_names = []

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
        self.move_names.append(str(self.board[chosen_move.new_pos.row][chosen_move.new_pos.col])+str(chosen_move))

    def act_on_move(self, move:Move):
        if type(move) != En_passant:
            new_board = copy.deepcopy(self.board)
            new_row, new_col = move.new_pos.row, move.new_pos.col
            old_row, old_col = move.prev.row, move.prev.col
            new_board[new_row][new_col] = copy.deepcopy(self.board[old_row][old_col])
            new_board[old_row][old_col] = Piece(color=Colors.blank)
            new_board[new_row][new_col].has_moved = True
            return new_board

        else:
            op = operator.sub if self.board[move.prev.row][move.prev.col].color == Colors.white else operator.add
            new_board = copy.deepcopy(self.board)
            new_row, new_col = move.new_pos.row, move.new_pos.col
            old_row, old_col = move.prev.row, move.prev.col
            new_board[new_row][new_col] = copy.deepcopy(self.board[old_row][old_col])
            new_board[old_row][old_col] = Piece(color=Colors.blank)
            new_board[new_row][new_col].has_moved = True

            # updating captured piece
            new_board[op(new_row, 1)][new_col] = Piece(color=Colors.blank)


def print_chess_board(board):
    for i in range(len(board)):
        print('\n')
        for j in range(len(board[0])):
            print(board[i][j], end='')
            print(board[i][j].color, end='\t')


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


def print_dots(number_of_dots):
    print('\r'+'*'* number_of_dots, end='')
    time.sleep(1)


if __name__ == '__main__':

    # num = 1
    # while 1:
    #     print_dots(number_of_dots=num)
    #     num += 1
    #     if num > 10:
    #         num = 1
    turn = Colors.white
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
        if turn == Colors.white:
            turn = Colors.black
        else:
            turn = Colors.white
        print_chess_board(game.board)
        print('\n')
        print('-' * 100)

    print(moves)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
