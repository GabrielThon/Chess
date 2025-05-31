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
        if not self.has_two_kings():
            raise exceptions.InvalidNumberOfKingsError()
        # The king of the player not playing must not be in check
        if self.king_in_check(next(iter(self.pieces[self.not_turn_to_move]["King"]))):
            raise exceptions.NonPlayingPlayerKingInCheckError(self.not_turn_to_move)
        # There should be no pawn on the 1st or 8th rank
        if self.has_pawn_on_first_eighth_rank():
            raise exceptions.PawnOnFirstOrEighthRowError()

    def has_two_kings(self) -> bool:
        for color in self.pieces.keys():
            if len(self.pieces[color]["King"]) != 1:
                return False
        return True

    def king_in_check(self, king: King) -> bool:
        if king.current_square in self.controlled_squares[king.opposite_color]:
            return True
        return False

    def has_pawn_on_first_eighth_rank(self):
        for color in self.pieces.keys():
            pawn_set = self.pieces[color]["Pawn"]
            for pawn in pawn_set:
                if pawn.current_square.row in [0, 7]:
                    return True
        return False


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
