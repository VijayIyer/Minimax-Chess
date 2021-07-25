# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Game import Game
from Colors import Colors
from Evaluator import ChessEvaluator
import copy
import math
import random as rnd
import time
from Board import Board


def save_game(game):
    with open('chess-game-sample.txt', 'w') as f:
        f.write(game.game_moves_total)


def Minimax(game, depth=0):
    scores = []
    if game.turn == Colors.white:
        moves = game.generate_moves()
        for move in moves:
            new_game = copy.deepcopy(game)
            new_game.update_board(move)
            if depth == 10:
                evaluator = ChessEvaluator(new_game)
                scores.append([(move, evaluator.evaluate())])
            else:
                new_game.turn = Colors.black
                scores.append((move, Minimax(new_game, depth + 1)))
                return max(scores)
        return [(None, -math.inf)]
    else:
        moves = game.generate_moves()
        for move in moves:

            game.update_board(move)
            if depth == 10:
                evaluator = ChessEvaluator(game)
                scores.append([(move, evaluator.evaluate())])
            else:
                game.turn = Colors.white
                scores.append((move, Minimax(game, depth + 1)))
                return min(scores)
        return [(None, -math.inf)]


def min_value(game, depth, alpha, beta):
    moves = game.generate_moves()
    if len(game.generate_moves()) == 0:
        return math.inf
    if depth >= 3:
        return ChessEvaluator(game).evaluate()
    v = math.inf
    for move in moves:
        game.update_board(move)
        v = min(v, max_value(game, depth+1, alpha, beta))
        game.revert_board(moves, move)
        if v <= alpha:
            return v
        beta = min([beta, v])
    return v


def max_value(game, depth, alpha, beta):
    moves = game.generate_moves()
    if len(game.generate_moves()) == 0:
        return -math.inf
    if depth >= 3:
        return ChessEvaluator(game).evaluate()
    v = -math.inf
    for move in moves:
        game.update_board(move)
        v = max(v, min_value(game, depth+1, alpha, beta))
        game.revert_board(moves, move)
        if v >= beta:
            return v
        alpha = max([alpha, v])
    return v


if __name__ == '__main__':
    # board = Board((8, 8))
    #
    # while(1):
    #     board.update_turn()
    #
    #     # move choosing logic, to be replaced by Minimax
    #     if board.turn == 'white':
    #         pieces = board.white_moves
    #     else:
    #         pieces = board.black_moves
    #     piece = rnd.choice(pieces.keys())
    #     move = rnd.choice(pieces[piece])
    #     board.add_move(piece, move)

    # diagonals = Board.generate_diagonals((8, 8))
    # straights = Board.get_rows_columns((8,8))
    # white_pos = Board.initialize_white_pos()
    # black_pos = Board.initalize_black_pos()
    # white_move_set = Board.generate_moves(white_pos)

    starting_pos = ['e4', 'e5']
    start = time.time()
    game = Game(starting_pos)

    game.max_moves = 10
    print(game.game_moves_total)
    while game.move_count <= game.max_moves:
        scores = []
        depth = 1
        valid_moves = game.generate_moves()
        for move in valid_moves:
            alpha = -math.inf
            beta = math.inf
            game.update_board(move)
            scores.append((move, min_value(game, depth + 1, alpha, beta)))
            game.revert_board(valid_moves, move)
        best_move = max(scores, key=lambda t: t[1])

        # best_move = Minimax(game)
        game.update_board(best_move[0])


    end = time.time() - start
    print(game.game_moves_total)
    print(end)
    # print(game.game_moves_total)
    # print_chess_board(game.board)
    # save_game(game)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
