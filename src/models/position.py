from src.models.board import Board, Square
from src.models.pieces import Piece, King, RecursiveControlledSquaresMixin
from src.models import exceptions


# State of the board
class Position:
    def __init__(self, board: Board, whose_move: str):
        self.pieces = dict.copy(board.pieces)
        self.whose_move = whose_move
        self.not_turn_to_move = "black" if self.whose_move == "white" else "black"
        # TO DO : Implement castling rights
        # TO DO : Implement en_passant (last piece_who_moved)

    def assert_valid_position(self):
        # Each player must have one king
        if not self.has_two_kings():
            raise exceptions.InvalidNumberOfKingsError()
        # The king of the player not playing must not be in check
        if self.king_in_check(next(iter(self.pieces[self.not_turn_to_move]["King"]))):
            raise exceptions.NonPlayingPlayerKingInCheckError(self.not_turn_to_move)
        # There should be no pawn on the 1st or 8th rank
        if self.has_pawn_on_first_eighth_rank():
            raise exceptions.PawnOnFirstOrEighthRowError()

    def is_valid_position(self):
        try:
            self.assert_valid_position()
        except exceptions.InvalidPositionError as e:
            print(e)
            return False
        else:
            return True

    def has_two_kings(self) -> bool:
        for color in self.pieces.keys():
            if len(self.pieces[color]["King"]) != 1:
                return False
        return True

    def king_in_check(self, king: King) -> bool:
        if king.current_square in self.controlled_squares(king.opposite_color):
            return True
        return False

    def has_pawn_on_first_eighth_rank(self):
        for color in self.pieces.keys():
            pawn_set = self.pieces[color]["Pawn"]
            for pawn in pawn_set:
                if pawn.current_square.row in [0, 7]:
                    return True
        return False

    def controlled_squares(self, color_string: str) -> set[Square]:
        return set().union(*(piece.controlled_squares() for piece_set in self.pieces[color_string].values() for piece in piece_set))

    def explore_checks_and_pins(self) -> [set["Piece"], set["Square"], dict["Piece", set["Square"]]]:
        pinned_pieces_squares_dict = {}
        checking_pieces = set()
        intercepting_squares = set()
        king = next(iter(self.pieces[self.whose_move]["King"]))
        for direction in king.moving_directions():
            squareset1, first_piece = king.current_square.explore_in_direction(direction)
            if not first_piece:
                continue
            if first_piece.color == king.opposite_color and isinstance(first_piece, RecursiveControlledSquaresMixin) and direction in first_piece.moving_directions():
                checking_pieces.add(first_piece)
                if len(checking_pieces) == 1:
                    intercepting_squares = squareset1
                else:
                    intercepting_squares = set()
            elif first_piece.color == king.color:
                squareset2, second_piece = first_piece.current_square.explore_in_direction(direction)
                if second_piece and second_piece.color == king.opposite_color and isinstance(second_piece, RecursiveControlledSquaresMixin) and direction in second_piece.moving_directions():
                    squareset = (squareset1 | squareset2)
                    squareset.remove(first_piece.current_square)
                    pinned_pieces_squares_dict[first_piece] = squareset if direction in first_piece.moving_directions() else set()
        return checking_pieces, intercepting_squares, pinned_pieces_squares_dict

    def legal_moves(self):
        # For now, assumes valid positions
        legal_moves = {}
        checking_pieces, intercepting_squares, pinned_pieces = self.explore_checks_and_pins()
        if len(checking_pieces) == 0:
            category = "no check"
        elif len(checking_pieces) == 1:
            category = "simple check"
        else:
            category = "double check"
        for piece in (p for s in self.pieces[self.whose_move].values() for p in s):
            if isinstance(piece, King):
                controlled_squares = self.controlled_squares(piece.opposite_color)
                legal_moves[piece] = piece.moving_squares() - controlled_squares
                continue
            if category == "double check":
                legal_moves[piece] = set()
                continue
            restricted_squares = pinned_pieces[piece] if piece in pinned_pieces.keys() else piece.controlled_squares()
            if category == "no check":
                legal_moves[piece] = restricted_squares
            else:  # category == "simple check" -> Intercepting squares
                legal_moves[piece] = restricted_squares & intercepting_squares
        return legal_moves


# Succession of positions
class Game:
    def __init__(self):
        self.positions = []
        pass

    def add_position(self, position: Position):
        self.positions.append(position)

    def get_position(self, halfmove_number: int):
        return self.positions[halfmove_number]

#
# if __name__ == "__main__":
#     position_text = {
#         "name": "pins_and_check_bishop",
#         "position": [
#             ["white", "King", "e1"],
#             ["black", "King", "e8"],
#             ["black", "Bishop", "a5"],
#             ["black", "Bishop", "h4"],
#             ["white", "Bishop", "c3"]
#         ],
#         "move": "white",
#         "result": [
#             ["white", "King", "e1", ["d1", "d2", "e2", "f1"]],
#             ["white", "Bishop", "c3", []]
#         ]
#     }
#
#     board = Board.create_empty_board()
#     for color, piece_type, square in position_text["position"]:
#         board.place(color, piece_type, square)
#
#     position = Position(board, position_text["move"])
#     position.legal_moves()
