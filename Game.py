from enum import Enum
import sys
import operator
import random as rnd
import numpy as np
import copy
import time
import Colors
from Colors import Colors
import Piece
import itertools
from Piece import Piece, Pawn, Queen, Knight, King, Bishop, Rook, is_in_check, get_king_pos
from Moves import Position, Move, En_passant, Capture, Castling, Promotion
import re
from collections import defaultdict


def find_piece_rows(piece_type, board, color):
    candidate_rows = []
    candidate_cols = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if type(board[i][j]) == piece_type and board[i][j].color == color:
                candidate_rows.append(i)
                candidate_cols.append(j)

    return candidate_rows, candidate_cols


def print_chess_board(board):
    for i in range(len(board)):
        print('\n')
        for j in range(len(board[0])):
            print(board[i][j], end='')
            print(board[i][j].color, end='\t')


def print_dots(number_of_dots):
    print('\r' + '*' * number_of_dots, end='')
    time.sleep(1)


class Game:
    def __init__(self, starting_pos):

        self.starting_pos = starting_pos
        self.board = self.initalize_board_and_pieces()
        self.moves = []
        self.move_names = []
        self.turn = Colors.white
        self.move_count = 1
        self.game_moves_total = ''
        self.is_in_check = ''
        self.same_move = defaultdict(list)
        if len(starting_pos) > 0:
            for move_name in starting_pos:

                move = self.infer_move(move_name, self.turn)
                self.update_board(move)
                # if self.turn == Colors.white:
                #     self.turn = Colors.black
                #     self.game_moves_total += ' ' + str(self.move_count) + '.'
                #     self.game_moves_total += self.move_names[-1]
                # elif self.turn == Colors.black:
                #     self.turn = Colors.white
                #
                #     self.game_moves_total += ' ' + self.move_names[-1]
                #     self.move_count += 1

    def get_move_name(self, chosen_move):
        promoted_piece = ''
        if type(chosen_move) == Promotion:
            if chosen_move.promote_to == Queen:
                promoted_piece = '=Q'
            elif chosen_move.promote_to == Rook:
                promoted_piece = '=R'
            elif chosen_move.promote_to == Knight:
                promoted_piece = '=N'
            elif chosen_move.promote_to == Bishop:
                promoted_piece = '=B'
            chosen_move = chosen_move.move
        tmp_moves = []
        # same piece check
        if type(self.board[chosen_move.prev.row][chosen_move.prev.col]) == Pawn:
            if chosen_move.prev.col == chosen_move.new_pos.col:
                return str(chosen_move) + promoted_piece
            else:
                return chr(96 + (8 - chosen_move.prev.col)) + str(chosen_move) + promoted_piece
        for move in self.same_move[(chosen_move.new_pos.row, chosen_move.new_pos.col)]:
            if type(move) != Promotion:
                if type(self.board[chosen_move.prev.row][chosen_move.prev.col]) == type(
                        self.board[move.prev.row][move.prev.col]):
                    tmp_moves.append(move)
        tmp_moves2 = []
        if len(tmp_moves) == 1:
            return str(self.board[chosen_move.prev.row][chosen_move.prev.col]) + str(chosen_move)
        # same col check
        else:
            for move in tmp_moves:
                if move.prev.col == chosen_move.prev.col:
                    tmp_moves2.append(move)
                #     return str(self.board[chosen_move.prev.row][chosen_move.prev.col]) + str(
                #         chosen_move.prev.row + 1) + str(chosen_move)
                # else:
                #     return str(self.board[chosen_move.prev.row][chosen_move.prev.col]) + chr(
                #         96 + (8 - chose
        col_amb = True
        if len(tmp_moves2) <= 1:
            col_amb = False
        # same row check
        if col_amb == False:
            return str(self.board[chosen_move.prev.row][chosen_move.prev.col]) + chr(
                96 + (8 - chosen_move.prev.col)) + str(chosen_move)

        tmp_moves3 = []
        row_amb = True
        for move in tmp_moves:
            if move.prev.row == chosen_move.prev.row:
                tmp_moves3.append(move)
        if len(tmp_moves3) <= 1:
            return str(self.board[chosen_move.prev.row][chosen_move.prev.col]) + str(chosen_move.prev.row + 1) + str(
                chosen_move)

        else:
            return str(self.board[chosen_move.prev.row][chosen_move.prev.col]) + chr(96 + (8 - chosen_move.prev.col)) \
                   + str(chosen_move.prev.row + 1) + str(chosen_move)

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

    def generate_moves(self):
        valid_moves = []
        self.same_move = defaultdict(list)
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col].color == self.turn:
                    piece = self.board[row][col]
                    valid_moves.extend(piece.get_moves(Position((row, col)), self))
        for move in valid_moves:
            if type(move) == Promotion:
                self.same_move[(move.move.new_pos.row, move.move.new_pos.col)].append(move)
                continue
            self.same_move[(move.new_pos.row, move.new_pos.col)].append(move)
        return valid_moves

    def update_board(self, chosen_move):
        if type(chosen_move) == Castling:
            self.move_names.append(str(chosen_move))
        else:
            self.move_names.append(self.get_move_name(chosen_move))
        self.board = self.act_on_move(chosen_move)
        self.moves.append(chosen_move)
        self.is_in_check = ''
        if is_in_check(self.board, Colors.white if self.turn == Colors.black else Colors.black,
                       get_king_pos(self.board, Colors.white if self.turn == Colors.black else Colors.black)):
            self.is_in_check = '+'
        if self.turn == Colors.white:
            self.game_moves_total += ' ' + str(self.move_count) + '.'
            self.game_moves_total += self.move_names[-1] + self.is_in_check
            self.turn = Colors.black

        else:
            self.turn = Colors.white
            self.game_moves_total += ' ' + self.move_names[-1] + self.is_in_check
            self.move_count += 1


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
        elif type(move) == Promotion:
            promoted_type = move.promote_to
            move = move.move
            new_board = copy.deepcopy(self.board)
            new_row, new_col = move.new_pos.row, move.new_pos.col
            old_row, old_col = move.prev.row, move.prev.col
            new_board[new_row][new_col] = promoted_type(color=new_board[old_row][old_col].color)
            new_board[old_row][old_col] = Piece(color=Colors.blank)
            new_board[new_row][new_col].has_moved = True
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
                             '?P<newrow>[1-8]{1})(?P<promotion>=([N|B|R|Q]){1})?(?P<checkormate>[+|#]?)$|('
                             '?P<LongCastle>^(O-O-O){1})$|(?P<Castle>^(O-O){1})$')
        m = re.match(pattern=pattern, string=move)
        m_dict = m.groupdict()
        piece_type = Pawn

        # region determining piece type
        if m_dict['piece'] != '':
            if m_dict['piece'] == 'R':
                piece_type = Rook
            elif m_dict['piece'] == 'Q':
                piece_type = Queen
            elif m_dict['piece'] == 'N':
                piece_type = Knight
            elif m_dict['piece'] == 'B':
                piece_type = Bishop
            else:
                piece_type = King
        # endregion

        promoted_piece = None
        if m_dict['LongCastle'] is not None:
            if color == Colors.white:
                self.same_move[(0, 5)].append(Castling(Position((0, 3)), Position((0, 5))))
                return Castling(Position((0, 3)), Position((0, 5)))
            elif color == Colors.black:
                self.same_move[(7, 5)].append(Castling(Position((7, 3)), Position((7, 5))))
                return Castling(Position((7, 3)), Position((7, 5)))
        if m_dict['Castle'] is not None:
            if color == Colors.white:
                self.same_move[(0, 1)].append(Castling(Position((0, 3)), Position((0, 1))))
                return Castling(Position((0, 3)), Position((0, 1)))
            elif color == Colors.black:
                self.same_move[(7, 1)].append(Castling(Position((7, 3)), Position((7, 1))))
                return Castling(Position((7, 3)), Position((7, 1)))

        # region determining prev column
        old_row, old_col = None, None
        if m_dict['amb'] != '':
            if m_dict['amb'] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                old_col = 104 - ord(m_dict['amb'])
            elif m_dict['amb'] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                old_row = int(m_dict['amb']) - 1
        # endregion
        # region determining move type
        if m_dict['capture'] != '':
            move_type = Capture
        else:
            move_type = Move
        # endregion
        if m_dict['promotion'] is not None:
            if m_dict['promotion'][1] == 'Q':
                promoted_piece = Queen
            if m_dict['promotion'][1] == 'R':
                promoted_piece = Rook
            if m_dict['promotion'][1] == 'N':
                promoted_piece = Knight
            if m_dict['promotion'][1] == 'B':
                promoted_piece = Bishop

        new_row, new_col = int(m_dict['newrow']) - 1, 104 - ord(m_dict['newcol'])

        candidate_rows, candidate_cols = find_piece_rows(piece_type, self.board, color)
        candidate_moves = []
        for row, col in zip(candidate_rows, candidate_cols):
            candidate_moves.extend(self.board[row][col].get_moves(Position((row, col)), self))

        if promoted_piece is not None:
            if (old_col is None and move_type == Capture) or (old_col is not None and move_type is not Capture):
                sys.exit('pawn cannot move diagonally without column being changed')
            elif old_col is None and move_type is not Capture:
                promotions = [move for move in candidate_moves if type(move) == Promotion]
                for promotion in promotions:
                    if piece_type == Pawn and promotion.move.new_pos.col == new_col and promotion.move.new_pos.row == new_row:
                        promoted_move = Promotion(move_type(promotion.move.prev, promotion.move.new_pos),
                                                  promote_to=promoted_piece)
                        self.same_move[(new_row, new_col)].append(promoted_move)
                        return promoted_move
            elif old_col is not None and move_type is Capture:
                promotions = [move for move in candidate_moves if type(move) == Promotion]
                for promotion in promotions:
                    if piece_type == Pawn and promotion.move.new_pos.col == new_col and promotion.move.new_pos.row == new_row and type(
                            promotion.move) == Capture and promotion.move.prev.col == old_col:
                        promoted_move = Promotion(move_type(promotion.move.prev, promotion.move.new_pos),
                                                  promote_to=promoted_piece)
                        self.same_move[(new_row, new_col)].append(promoted_move)
                        return promoted_move

        candidate_moves = [move for move in candidate_moves if type(move) != Promotion]

        if len(candidate_moves) == 0:
            sys.exit('no such move possible from any piece - {0}'.format(move))
            return []

        moves_with_same_pos = []
        tmp_move_type = move_type
        for move in candidate_moves:
            if type(move) == En_passant and move_type == Capture:
                tmp_move_type = En_passant
            if move.new_pos.row == new_row and move.new_pos.col == new_col and type(
                    self.board[move.prev.row][move.prev.col]) == piece_type:
                moves_with_same_pos.append(tmp_move_type(move.prev, move.new_pos))
            tmp_move_type = move_type

        final_list = []
        if len(moves_with_same_pos) == 1:
            self.same_move[(moves_with_same_pos[0].new_pos.row, moves_with_same_pos[0].new_pos.col)].append(
                moves_with_same_pos[0])
            return moves_with_same_pos[0]
        else:
            if old_col is None and old_row is None:
                raise Exception('more than one move with same piece and ')
            elif old_col is not None:
                for move in moves_with_same_pos:
                    if move.prev.col == old_col:
                        final_list.append(move)
            elif old_row is not None:
                for move in moves_with_same_pos:
                    if move.prev.row == old_row:
                        final_list.append(move)

        if len(final_list) > 1:
            raise Exception('move is still ambiguous')
        else:
            return final_list[0]

    def next_move(self):

        moves = self.generate_moves()
        if len(moves) == 0:
            if self.is_in_check == '+':
                self.is_in_check = '#'
                self.game_moves_total += self.is_in_check
                print(f'\n---game over---{self.turn} loses')
            else:
                print('\n----stalemate----')
        else:
            self.game_moves_total += self.is_in_check

        self.update_board(rnd.choice(moves))
        if self.turn == Colors.white:
            self.game_moves_total += ' ' + str(self.move_count) + '.'
            self.game_moves_total += self.move_names[-1]
            self.turn = Colors.black
            # print(game.game_moves_total)

        else:
            self.turn = Colors.white
            self.game_moves_total += ' ' + self.move_names[-1]
            # print(game.game_moves_total)

            self.move_count += 1 # increase move count only when both black and white have completed turns