# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Game import Game
from Colors import Colors
from Evaluator import ChessEvaluator
import copy
import math
import random as rnd


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
            new_game = copy.deepcopy(game)
            new_game.update_board(move)
            if depth == 10:
                evaluator = ChessEvaluator(new_game)
                scores.append([(move, evaluator.evaluate())])
            else:
                new_game.turn = Colors.white
                scores.append((move, Minimax(new_game, depth + 1)))
                return min(scores)
        return [(None, -math.inf)]


def min_value(new_game, depth):
    moves = new_game.generate_moves()
    if len(new_game.generate_moves()) == 0:
        return math.inf
    if depth >= 3:
        return ChessEvaluator(new_game).evaluate()
    v = math.inf
    for move in moves:
        game = copy.deepcopy(new_game)
        game.update_board(move)
        v = min(v, max_value(game, depth+1))
    return v


def max_value(new_game, depth):
    moves = new_game.generate_moves()
    if len(new_game.generate_moves()) == 0:
        return -math.inf
    if depth >= 3:
        return ChessEvaluator(new_game).evaluate()
    v = -math.inf
    for move in moves:
        game = copy.deepcopy(new_game)
        game.update_board(move)
        v = max(v, min_value(game, depth+1))
    return v


if __name__ == '__main__':
    starting_pos = ['e4', 'e5', 'Qh5', 'Nf6']

    game = Game(starting_pos)

    game.max_moves = 5
    print(game.game_moves_total)
    while game.move_count <= game.max_moves:
        scores = []
        depth = 0
        for move in game.generate_moves():
            new_game = copy.deepcopy(game)
            new_game.update_board(move)
            scores.append((move, min_value(new_game, depth + 1)))
        best_move = max(scores, key=lambda t: t[1])

        # best_move = Minimax(game)
        game.update_board(best_move[0])

    # print(game.game_moves_total)
    # print_chess_board(game.board)
    save_game(game)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
