from src.models.board import Board
from src.models.pieces import Pawn, King
from src.models import exceptions


# State of the board
class Position:
    def __init__(self, board: Board, whose_move: str):
        self.pieces = dict.copy(board.pieces)
        self.controlled_squares = {"white": board.controlled_squares("white"),
                                   "black": board.controlled_squares("black")}
        self.whose_move = whose_move
        self.not_turn_to_move = "black" if self.whose_move == "white" else "black"
        # TO DO : Implement castling rights
        # TO DO : Implement en_passant (last piece_who_moved)

    def assert_valid_position(self):
        # Each player must have one king
        kings = self.assert_has_two_kings()
        # The king of the player not playing must not be in check
        if self.king_in_check(kings[self.not_turn_to_move]):
            raise exceptions.NonPlayingPlayerKingInCheckError(self.not_turn_to_move)
        # There should be no pawn on the 1st or 8th rank
        self.assert_no_pawn_on_first_eighth_rank()

    def assert_has_two_kings(self) -> dict[str, King]:
        # If each player has a king, returns a dict [color, king], otherwise raises an error
        kings = {}
        for color in self.pieces.keys():
            king_set = self.pieces[color]["King"]
            if len(self.pieces[color]["King"]) != 1:
                raise exceptions.InvalidNumberOfKingsError()
            else:
                kings[color] = next(iter(king_set))
        return kings

    def king_in_check(self, king: King) -> bool:
        if king.current_square in self.controlled_squares[king.opposite_color]:
            return True
        return False

    def assert_no_pawn_on_first_eighth_rank(self):
        pawns = {
            color: [piece for piece in pieces.values() if isinstance(piece, Pawn)]
            for color, pieces in self.pieces.items()
        }
        for pawn_list in pawns.values():
            for pawn in pawn_list:
                if pawn.current_square.row in [0, 7]:
                    raise exceptions.PawnOnFirstOrEighthRowError(pawn)

    def is_valid_position(self):
        try:
            self.assert_valid_position()
        except exceptions.InvalidPositionError as e:
            print(e)
            return False
        else:
            return True


# Succession of positions
class Game:
    def __init__(self):
        self.positions = []
        pass

    def add_position(self, position: Position):
        self.positions.append(position)

    def get_position(self, halfmove_number: int):
        return self.positions[halfmove_number]
