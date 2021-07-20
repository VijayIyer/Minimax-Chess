from collections import defaultdict
from Colors import Colors
from Piece import Pawn, Bishop, Knight, Queen, King, Rook


class ChessEvaluator:
    def __init__(self, game):
        self.game = game
        self.material_value = defaultdict(int)

    def evaluate(self):
        for i, row in enumerate(self.game.board):
            for j, piece in enumerate(row):
                if piece.color != Colors.blank:
                    if type(piece) == Pawn:
                        self.material_value[piece.color] += 1
                    if type(piece) in [Bishop,Knight]:
                        self.material_value[piece.color] += 3
                    if type(piece) == Rook:
                        self.material_value[piece.color] += 5
                    if type(piece) == Queen:
                        self.material_value[piece.color] += 9

        return self.material_value[Colors.white] - self.material_value[Colors.black]