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
import sys


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
    num_moves = int(sys.argv[1])
    move_logic = sys.argv[2]

    starting_pos = []
    start = time.time()
    game = Game(starting_pos)

    game.max_moves = num_moves
    print(game.game_moves_total)
    while game.move_count <= game.max_moves:
        scores = []
        depth = 1
        valid_moves = game.generate_moves()
        if len(valid_moves) == 0 : break
        if move_logic == 'minimax':
            for move in valid_moves:
                alpha = -math.inf
                beta = math.inf
                game.update_board(move)
                scores.append((move, min_value(game, depth + 1, alpha, beta)))
                game.revert_board(valid_moves, move)
            best_move = max(scores, key=lambda t: t[1])

            best_move = Minimax(game)
        else:
            game.update_board(rnd.choice(valid_moves))


    end = time.time() - start
    print(game.game_moves_total)
    print(end)
    # print(game.game_moves_total)
    # print_chess_board(game.board)
    save_game(game)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
