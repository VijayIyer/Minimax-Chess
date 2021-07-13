import operator
from Colors import Colors
from Moves import Move, Position, Capture, Castling, En_passant
import copy
import itertools

class Piece:
    def __init__(self, color, is_pinned=False):
        self.is_pinned = is_pinned
        self.color = color
        self.has_moved = False

    def get_moves(self, position, board):
        return []

    def __str__(self):
        return ''


def get_king_pos(pretend_board, color):
    for row in range(len(pretend_board)):
        for col in range(len(pretend_board[0])):
            if type(pretend_board[row][col]) == King and pretend_board[row][col].color == color:
                return row, col


def is_in_check(pretend_board, color, pos):
    """

    :param pretend_board: a board with a move made to check whether king is attacked
    :param color: to check the king of given color for check
    :return: whether king of color is in check or not after candidate move on the pretend_board
    """

    # move itself is not valid if piece moves to the same place as king
    if pos is None:
        return True

    row, col = pos[0], pos[1]

    # checking in 8 directions for opposing piece
    for i in range(row + 1, len(pretend_board)):
        if 0 <= i <= 7 and pretend_board[i][col].color not in [color, Colors.blank] and type(pretend_board[i][col]) in [Rook, Queen]:
            return True
        if pretend_board[i][col].color == color:
            break

    for i in range(row - 1, 0, -1):
        if 0 <= i <= 7 and pretend_board[i][col].color not in [color, Colors.blank] and type(pretend_board[i][col]) in [Rook, Queen]:
            return True
        if 0 <= i <= 7 and pretend_board[i][col].color == color:
            break

    for i in range(col + 1, len(pretend_board)):
        if 0 <= i <= 7 and pretend_board[row][i].color not in [color, Colors.blank] and type(pretend_board[row][i]) in [Rook, Queen]:
            return True
        if 0 <= i <= 7 and pretend_board[row][i].color == color:
            break

    for i in range(col - 1, 0, -1):
        if 0 <= i <= 7 and pretend_board[row][i].color not in [color, Colors.blank] and type(pretend_board[row][i]) in [Rook, Queen]:
            return True
        if 0 <= i <= 7 and pretend_board[row][i].color == color:
            break
    i = 1

    while 0 <= row - i <= 7 and 0 <= col - i <= 7:
        if pretend_board[row - i][col - i].color not in [color, Colors.blank] and type(
                pretend_board[row - i][col - i]) in [Bishop, Queen]:
            return True
        if pretend_board[row - i][col - i].color == color:
            break
        i += 1
    i = 1
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
        j += 1
    i = 1
    j = 1
    while 0 <= row - i <= 7 and 0 <= col + j <= 7:
        if pretend_board[row - i][col + j].color not in [color, Colors.blank] \
                and type(pretend_board[row - i][col + j]) in [Bishop, Queen]:
            return True
        if pretend_board[row - i][col + j].color == color:
            break
        i += 1
        j += 1

    # check by pawn
    if color == Colors.white:
        for i in [-1, 1]:
            if 0 <= row+1 <= 7 and 0 <= col+i <= 7 and pretend_board[row + 1][col + i].color not in [color, Colors.blank] and type(
                    pretend_board[row + 1][col + i]) == Pawn:
                return True
    if color == Colors.black:
        for i in [-1, 1]:
            if 0 <= row-1 <= 7 and 0 <= col+i <= 7 and pretend_board[row - 1][col + i].color not in [color, Colors.blank] and type(
                    pretend_board[row - 1][col + i]) == Pawn:
                return True

    for i, j in itertools.product([-2,2],[-1,1]):
        if 0 <= row+i <= 7 and 0 <= col+j <= 7 and pretend_board[row+i][col+j].color not in [Colors.blank, color] and type(pretend_board[row+i][col+j]) == Knight:
            return True

    for i, j in itertools.product([-1, 1], [-2, 2]):
        if 0 <= row+i <= 7 and 0 <= col+j <= 7 and pretend_board[row + i][col + j].color not in [Colors.blank, color] and type(
                pretend_board[row + i][col + j]) == Knight:
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
            color = board[move.prev.row][move.prev.col].color

            pretend_board = copy.deepcopy(board)
            old_piece = pretend_board[move.prev.row][move.prev.col]
            pretend_board[move.prev.row][move.prev.col] = Piece(color=Colors.blank)
            pretend_board[move.new_pos.row][move.new_pos.col] = old_piece
            pos = get_king_pos(pretend_board, color)
            if pos is not None:

                # if move.prev.row+move.prev.col != pos[0]+pos[1] and \
                #         move.prev.row - move.prev.col != pos[0] - pos[1]\
                #         and move.prev.row != pos[0] and move.prev.col != pos[1]:
                #     valid_moves.append(move)
                if not is_in_check(pretend_board, color, pos):
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
            if prev_move.new_pos.row == move.new_pos.row:
                if color == Colors.black:
                    if move.prev.col == prev_move.new_pos.col + 1 and move.new_pos.col == prev_move.new_pos.col:
                        if prev_move.prev.row == prev_move.new_pos.row - 2 and prev_move.new_pos.col == prev_move.prev.col:
                            valid_moves.append(move)
                    if move.prev.col == prev_move.new_pos.col - 1 and move.new_pos.col == prev_move.new_pos.col:
                        if prev_move.prev.row == prev_move.new_pos.row - 2 and prev_move.new_pos.col == prev_move.prev.col:
                            valid_moves.append(move)

                if color == Colors.white:
                    if move.prev.col == prev_move.new_pos.col + 1 and move.new_pos.col == prev_move.new_pos.col:
                        if prev_move.prev.row == prev_move.new_pos.row + 2 and prev_move.new_pos.col == prev_move.prev.col:
                            valid_moves.append(move)
                    if move.prev.col == prev_move.new_pos.col - 1 and move.new_pos.col == prev_move.new_pos.col:
                        if prev_move.prev.row == prev_move.new_pos.row + 2 and prev_move.new_pos.col == prev_move.prev.col:
                            valid_moves.append(move)
            # if color == Colors.white and prev_move.new_pos.row == prev_move.prev.row - 2 and (prev_move.new_pos.col == prev_col+1 or prev_move.new_pos.col == prev_col-1) and move.new_pos.col == prev_move.new_pos.col:
            #     if type(board[move.prev.row][move.prev.col-1]) == Pawn and board[move.prev.row][move.prev.col+1].color not in [Colors.blank, color]:
            #         valid_moves.append(move)
            #     elif type(board[move.prev.row][move.prev.col+1]) == Pawn and board[move.prev.row][move.prev.col+1].color not in [Colors.blank, color]:
            #         valid_moves.append(move)
            #
            # if color == Colors.black and prev_move.new_pos.row == prev_move.prev.row + 2 and (prev_move.prev.col == prev_col+1 or prev_move.prev.col == prev_col-1) and move.new_pos.col == prev_move.new_pos.col:
            #     if type(board[move.prev.row][move.prev.col-1]) == Pawn and board[move.prev.row][move.prev.col-1].color not in [Colors.blank, color]:
            #         valid_moves.append(move)
            #     elif type(board[move.prev.row][move.prev.col+1]) == Pawn and board[move.prev.row][move.prev.col+1].color not in [Colors.blank, color]:
            #         valid_moves.append(move)

    return valid_moves


def filter_bishop_moves(board, candidate_moves):
    valid_moves = []
    tmp_row, tmp_col = None, None
    for move in candidate_moves:
        new_row, new_col = move.new_pos.row, move.new_pos.col
        old_row, old_col = move.prev.row, move.prev.col
        # (bad coding) original position cut off from new position - not valid for rook and bishop
        if tmp_row is not None and tmp_col is not None:
            if new_row > tmp_row + 1 or new_row < tmp_row - 1 or new_col > tmp_col + 1 or new_col < tmp_col - 1:
                break
        else:
            if new_row > old_row + 1 or new_row < old_row - 1 or new_col > old_col + 1 or new_col < old_col - 1:
                break

        if board[new_row][new_col].color == board[old_row][old_col].color:
            break
        if board[new_row][new_col].color not in [Colors.blank, board[old_row][old_col].color]:
            valid_moves.append(Capture(move.prev, move.new_pos))
            break
        valid_moves.append(move)
        tmp_row, tmp_col = new_row, new_col
    return valid_moves


def filter_knight_moves(board, candidate_moves):
    valid_moves = []
    for move in candidate_moves:
        new_row, new_col = move.new_pos.row, move.new_pos.col
        old_row, old_col = move.prev.row, move.prev.col
        if board[new_row][new_col].color == Colors.blank:
            valid_moves.append(move)
        if board[new_row][new_col].color not in [Colors.blank, board[old_row][old_col].color]:
            valid_moves.append(Capture(move.prev, move.new_pos))

    return valid_moves


def filter_castling_moves(board, castling_moves):
    valid_moves = []
    move1, move2 = castling_moves[0], castling_moves[1]
    color = board[move1.prev.row][move1.prev.col].color

    row, col = get_king_pos(board, color)
    if board[row][col].has_moved:
        return []

    # for short castling

    if type(board[row][col - 3]) is Rook and not board[row][col - 3].has_moved:
        for i in range(1, 3):

            if board[row][col - i].color != Colors.blank or is_in_check(board, color, (row, col - i)):
              break
        else:
            valid_moves.append(move2)

    # for long castling

    if type(board[row][col + 4]) is Rook and not board[row][col + 4].has_moved:
        for i in range(1, 3):
            if board[row][col + i].color != Colors.blank or is_in_check(board, color, (row, col+i)):
                break
        else:
            valid_moves.append(move1)

    return valid_moves


def filter_pawn_moves(board, normal_moves):
    valid_moves = []
    for move in normal_moves:
        if board[move.new_pos.row][move.new_pos.col].color == Colors.blank:
            valid_moves.append(move)
    return valid_moves


class Pawn(Piece):
    def __init__(self, color, is_pinned=False):
        super(Pawn, self).__init__(color, is_pinned)

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
        if not self.has_moved:
            num_steps = 2
        else:
            num_steps = 1
        normal_moves = [Move(position, Position((op(row,i), col))) for i in range(1, num_steps+1)]
        normal_moves = filter_valid_moves(game.board, normal_moves)
        capture_moves = [Capture(position, Position((op(row,1), col + i))) for i in [-1, 1]]
        capture_moves = filter_valid_moves(game.board, capture_moves)
        en_passant_moves = [En_passant(position, Position((op(row, 1), col + 1))),En_passant(position, Position((op(row, 1), col - 1)))]
        en_passant_moves = filter_valid_moves(game.board, en_passant_moves)

        normal_moves = filter_pawn_moves(game.board, normal_moves)
        capture_moves = filter_pawn_captures(game.board, capture_moves)
        en_passant_moves = filter_en_passant(game, en_passant_moves)

        return normal_moves + capture_moves + en_passant_moves

    def __str__(self):
        return ''


class Rook(Piece):
    def __init__(self, color, is_pinned=False):
        super(Rook, self).__init__(color, is_pinned)

    def get_moves(self, position, game):
        row = position.row
        col = position.col

        right_up_moves = filter_valid_moves(game.board, [Move(position, Position((row+i, col))) for i in range(1, len(game.board))])
        right_down_moves = filter_valid_moves(game.board, [Move(position, Position((row - i, col))) for i in range(1, len(game.board))])
        left_up_moves = filter_valid_moves(game.board, [Move(position, Position((row, col-i))) for i in range(1, len(game.board))])
        left_down_moves = filter_valid_moves(game.board, [Move(position, Position((row, col+i))) for i in range(1, len(game.board))])

        right_up_moves = filter_bishop_moves(game.board, right_up_moves)
        right_down_moves = filter_bishop_moves(game.board, right_down_moves)
        left_up_moves = filter_bishop_moves(game.board, left_up_moves)
        left_down_moves = filter_bishop_moves(game.board, left_down_moves)

        return right_up_moves+right_down_moves+left_up_moves+left_down_moves

    def __str__(self):
        return 'R'


class King(Piece):
    def __init__(self, color, is_pinned=False):
        super(King, self).__init__(color, is_pinned)

    def get_moves(self, position, game):
        row = position.row
        col = position.col

        normal_moves = [Move(position, Position((row+i, col+j))) for i, j in itertools.product([0, 1, -1],repeat=2)]
        normal_moves = filter_valid_moves(game.board, normal_moves)
        normal_moves = filter_knight_moves(game.board, normal_moves)

        castling_moves = [Castling(position, Position((row, col+2))), Castling(position, Position((row, col - 2)))]
        castling_moves = filter_castling_moves(game.board, castling_moves)

        return normal_moves + castling_moves

    def __str__(self):
        return 'K'


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

    def __str__(self):
        return 'B'


class Queen(Piece):
    def __init__(self, color, is_pinned=False):
        super(Queen, self).__init__(color, is_pinned)

    def get_moves(self, position, game):
        color = game.board[position.row][position.col].color
        bishop = Bishop(color)
        rook = Rook(color)
        return bishop.get_moves(position, game) + rook.get_moves(position, game)

    def __str__(self):
        return 'Q'


class Knight(Piece):
    def __init__(self, color, is_pinned=False):
        super(Knight, self).__init__(color, is_pinned)

    def get_moves(self, position, game):
        row = position.row
        col = position.col
        a = [-2, 2]
        b = [-1, 1]
        moves_1 = [Move(position, Position((row+i, col+j))) for i, j in itertools.product(a, b)]
        a = [-1, 1]
        b = [-2, 2]
        moves_2 = [Move(position, Position((row+i, col+j))) for i, j in itertools.product(a, b)]
        knight_moves = filter_valid_moves(game.board, moves_1+moves_2)
        knight_moves = filter_knight_moves(game.board, knight_moves)
        return knight_moves

    def __str__(self):
        return 'N'

