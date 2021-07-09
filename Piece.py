import operator
from Colors import Colors
from Moves import Move, Position, Capture, Castling, En_passant
import copy


class Piece:
    def __init__(self, color, is_pinned=False):
        self.is_pinned = is_pinned
        self.color = color

    def get_moves(self, position, board):
        return []


def get_king_pos(pretend_board, color):
    for row in range(len(pretend_board)):
        for col in range(len(pretend_board[0])):
            if type(pretend_board[row][col]) == King and pretend_board[row][col].color == color:
                return row, col


def is_in_check(pretend_board, color):
    """

    :param pretend_board: a board with a move made to check whether king is attacked
    :param color: to check the king of given color for check
    :return: whether king of color is in check or not after candidate move on the pretend_board
    """

    row, col = get_king_pos(pretend_board, color)
    i = 1
    j = 1
    # checking in 8 directions for opposing piece
    for i in range(row + 1, len(pretend_board)):
        if 0 <= i <= 7 and pretend_board[i][col].color not in [color, Colors.blank] and type(pretend_board[i][col]) in [Rook, Queen]:
            return True
        if pretend_board[i][col].color == color:
            break
    i = 1
    j = 1
    for i in range(row - 1, 0, -1):
        if 0 <= i <= 7 and pretend_board[i][col].color not in [color, Colors.blank]:
            return True
        if 0 <= i <= 7 and pretend_board[i][col].color == color:
            break
    i = 1
    j = 1
    for i in range(col + 1, len(pretend_board)):
        if 0 <= i <= 7 and pretend_board[row][i].color not in [color, Colors.blank]:
            return True
        if 0 <= i <= 7 and pretend_board[row][i].color == color:
            break
    i = 1
    j = 1
    for i in range(col - 1, 0, -1):
        if 0 <= i <= 7 and pretend_board[row][i].color not in [color, Colors.blank]:
            return True
        if 0 <= i <= 7 and pretend_board[row][i].color == color:
            break
    i = 1
    j = 1
    while 0 <= row - i <= 7 and 0 <= col - i <= 7:
        if pretend_board[row - i][col - i].color not in [color, Colors.blank] and type(
                pretend_board[row - i][col - i]) in [Bishop, Queen]:
            return True
        if pretend_board[row - i][col - i].color == color:
            break
        i -= 1
    i = 1
    j = 1
    while 0 <= row + i <= 7 and 0 <= col + i <= 7:
        if pretend_board[row + i][col + i].color not in [color, Colors.blank] and type(
                pretend_board[row + i][col + i]) in [Bishop, Queen]:
            return True
        if pretend_board[row + i][col + i].color == color:
            break
        i += 1
    i = 1
    j = 1
    while 0 <= row + i <= 7 and 0 <= col - j <= 7:
        if pretend_board[row + i][col - j].color not in [color, Colors.blank] \
                and type(pretend_board[row + i][col - j]) in [Bishop, Queen]:
            return True
        if pretend_board[row + i][col - j].color == color:
            break
        i += 1
        j -= 1
    i = 1
    j = 1
    while 0 <= row - i <= 7 and 0 <= col + j <= 7:
        if pretend_board[row - i][col + j].color not in [color, Colors.blank] \
                and type(pretend_board[row - i][col + j]) in [Bishop, Queen]:
            return True
        if pretend_board[row - i][col + j].color == color:
            break
        i -= 1
        j += 1

    # check by pawn
    if color == Colors.white:
        for i in [-1, 1]:
            if pretend_board[row + 1][col + i].color not in [color, Colors.blank] and type(
                    pretend_board[row + 1][col + i]) == Pawn:
                return True
    if color == Colors.black:
        for i in [-1, 1]:
            if pretend_board[row - 1][col + i].color not in [color, Colors.blank] and type(
                    pretend_board[row - 1][col + i]) == Pawn:
                return True

    return False


def filter_valid_moves(board, candidate_moves):
    """
    :param board: the 8x8 board containing all pieces
    :param candidate_moves: moves allowed for pawn, irrespective of neighboring squares and bounds
    :return: valid moves within bounds of the board and not pinned (king is not in check after the move)
    """
    valid_moves = []
    for move in candidate_moves:
        if 0 <= move.new_pos.row <= len(board)-1 and 0 <= move.new_pos.col <= len(board[0])-1:
            pretend_board = copy.deepcopy(board)
            old_piece = pretend_board[move.prev.row][move.prev.col]
            pretend_board[move.prev.row][move.prev.col] = Piece(color=Colors.blank)
            pretend_board[move.new_pos.row][move.new_pos.col] = old_piece
            if not is_in_check(pretend_board, old_piece.color):
                valid_moves.append(move)
    return valid_moves


def filter_pawn_captures(board, candidate_moves):
    """
    :param board: the 8x8 grid
    :param candidate_moves: moves passed in which are within bounds of the board
    :return: list of moves after removing captures which are not valid - same color piece or no piece on diagonal
    """
    valid_moves = []
    for move in candidate_moves:
        if type(move) == Capture:
            if board[move.new_pos.row][move.new_pos.col].color not in [Colors.blank, board[move.prev.row][move.prev.col].color]:
                valid_moves.append(move)

    return valid_moves


def filter_en_passant(game, candidate_moves):
    board = game.board
    prev_move = game.moves[-1] if len(game.moves) > 0 else None
    valid_moves = []
    # special case of 1st move
    if prev_move is None:
        return []

    for move in candidate_moves:
        prev_row, prev_col = move.prev.row, move.prev.col
        color = board[prev_row][prev_col].color
        if type(move) == En_passant:

            if color == Colors.white and prev_move.prev.row == prev_row + 2 and (prev_move.prev.col == prev_col+1 or prev_move.prev.col  == prev_col-1):
                if type(board[prev_row][prev_col-1]) != Pawn or board[prev_row][prev_col-1].color in [Colors.blank, color]:
                    valid_moves.append(move)
                elif type(board[prev_row][prev_col+1]) != Pawn or board[prev_row][prev_col+1].color in [Colors.blank, color]:
                    valid_moves.append(move)

            if color == Colors.black and prev_move.prev.row == prev_row - 2 and (prev_move.prev.col == prev_col+1 or prev_move.prev.col  == prev_col-1):
                if type(board[prev_row][prev_col-1]) == Pawn and board[prev_row][prev_col-1].color in [Colors.blank, color]:
                    valid_moves.append(move)
                elif type(board[prev_row][prev_col-1]) == Pawn and board[prev_row][prev_col+1].color in [Colors.blank, color]:
                    valid_moves.append(move)

    return valid_moves


def filter_bishop_moves(board, candidate_moves):
    valid_moves = []
    for move in candidate_moves:
        new_row, new_col = move.new_pos.row, move.new_pos.col
        old_row, old_col = move.prev.row, move.prev.col
        if board[new_row][new_col].color == board[old_row][old_col].color:
            break
        if board[new_row][new_col].color not in [Colors.blank, board[old_row][old_col].color]:
            valid_moves.append(Capture(move.prev, move.new_pos))
            break
        valid_moves.append(move)

    return valid_moves


class Pawn(Piece):
    def __init__(self, color, is_pinned=False):
        super(Pawn, self).__init__(color, is_pinned)
        self.moved_once = False

    def get_moves(self, position, game):
        row = position.row
        col = position.col

        if self.color == Colors.white:
            # white moves forward
            op = operator.add
        else:
            # black moves in opposite direction of white
            op = operator.sub

        # move only valid if pawn hasnt moved yet
        if not self.moved_once:
            num_steps = 2
        else:
            num_steps = 1
        normal_moves = [Move(position, Position((op(row,i), col))) for i in range(1, num_steps+1)]
        normal_moves = filter_valid_moves(game.board, normal_moves)
        capture_moves = [Capture(position, Position((op(row,1), col + i))) for i in [-1, 1]]
        capture_moves = filter_valid_moves(game.board, capture_moves)
        en_passant_moves = [En_passant(position, Position((op(row, 1), col + 1))),En_passant(position, Position((op(row, 1), col - 1)))]
        en_passant_moves = filter_valid_moves(game.board, en_passant_moves)

        capture_moves = filter_pawn_captures(game.board, capture_moves)
        en_passant_moves = filter_en_passant(game, en_passant_moves)

        return normal_moves + capture_moves + en_passant_moves


class Rook(Piece):
    def __init__(self, color, is_pinned=False):
        super(Rook, self).__init__(color, is_pinned)
        self.has_moved = False

    def get_moves(self, position, game):
        row = position.row
        col = position.col

        right_up_moves = filter_valid_moves(game.board, [Move(position, Position((row+i, col))) for i in range(1, len(game.board) - 1)])
        right_down_moves = filter_valid_moves(game.board, [Move(position, Position((row - i, col))) for i in range(1, len(game.board) - 1)])
        left_up_moves = filter_valid_moves(game.board, [Move(position, Position((row, col-i))) for i in range(1, len(game.board) - 1)])
        left_down_moves = filter_valid_moves(game.board, [Move(position, Position((row, col+i))) for i in range(1, len(game.board) - 1)])

        right_up_moves = filter_bishop_moves(game.board, right_up_moves)
        right_down_moves = filter_bishop_moves(game.board, right_down_moves)
        left_up_moves = filter_bishop_moves(game.board, left_up_moves)
        left_down_moves = filter_bishop_moves(game.board, left_down_moves)

        return right_up_moves+right_down_moves+left_up_moves+left_down_moves


class King(Piece):
    def __init__(self, color, is_pinned=False):
        super(King, self).__init__(color, is_pinned)
        self.has_moved = False


class Bishop(Piece):
    def __init__(self, color, is_pinned=False):
        super(Bishop, self).__init__(color, is_pinned)

    def get_moves(self, position, game):
        row = position.row
        col = position.col

        right_up_moves = filter_valid_moves(game.board, [Move(position, Position((row+i, col+i))) for i in range(1, len(game.board) - 1)])
        right_down_moves = filter_valid_moves(game.board, [Move(position, Position((row - i, col + i))) for i in range(1, len(game.board) - 1)])
        left_up_moves = filter_valid_moves(game.board, [Move(position, Position((row+i, col-i))) for i in range(1, len(game.board) - 1)])
        left_down_moves = filter_valid_moves(game.board, [Move(position, Position((row-i, col-i))) for i in range(1, len(game.board) - 1)])

        right_up_moves = filter_bishop_moves(game.board, right_up_moves)
        right_down_moves = filter_bishop_moves(game.board, right_down_moves)
        left_up_moves = filter_bishop_moves(game.board, left_up_moves)
        left_down_moves = filter_bishop_moves(game.board, left_down_moves)

        return right_up_moves+right_down_moves+left_up_moves+left_down_moves


class Queen(Piece):
    def __init__(self, color, is_pinned=False):
        super(Queen, self).__init__(color, is_pinned)

    def get_moves(self, position, game):
        color = game.board[position.row][position.col].color
        bishop = Bishop(color)
        rook = Rook(color)
        return bishop.get_moves(position, game) + rook.get_moves(position, game)


class Knight(Piece):
    def __init__(self, color, is_pinned=False):
        super(Knight, self).__init__(color, is_pinned)

    def get_moves(self, position, game):
        row = position.row
        col = position.col
        a = [-2, 2]
        b = [-1, 1]
        moves_1 = [Move(position, Position((row+i, col+j))) for i, j in zip(a, b)]
        a = [-1, 1]
        b = [-2, 2]
        moves_2 = [Move(position, Position((row+i, col+j))) for i, j in zip(a, b)]
        knight_moves = filter_valid_moves(game.board, moves_1+moves_2)
        knight_moves = filter_bishop_moves(game.board, knight_moves)
        return knight_moves
