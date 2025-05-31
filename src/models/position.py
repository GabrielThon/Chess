from src.models.board import Board
from src.models.pieces import Pawn, King
from src.models import exceptions

#State of the board
class Position:
    def __init__(self, board: Board, whose_move: str):
        self.pieces = dict.copy(board.pieces)
        self.controlled_squares = {"white" : board.controlled_squares("white"),
                                   "black" : board.controlled_squares("black")}
        self.whose_move = whose_move
        self.not_turn_to_move = "black" if self.whose_move == "white" else "black"
        #TO DO : Implement castling rights
        #TO DO : Implement en_passant (last piece_who_moved)

    def assert_valid_position(self):
        #Each player must have a single king
        kings = {
            color: [piece for piece in pieces.values() if isinstance(piece, King)]
            for color, pieces in self.pieces.items()
        }
        nb_kings = {"white" :len(kings["white"]),
                    "black" :len(kings["black"])}
        for nb_king in nb_kings.values():
            if nb_king != 1:
                raise exceptions.InvalidNumberOfKingsError(nb_kings)

        #The king of the player not playing must not be in check
        if kings[self.not_turn_to_move][0].current_square in self.controlled_squares[self.whose_move]:
            raise exceptions.NonPlayingPlayerKingInCheckError(self.not_turn_to_move)

        #There should be no pawn on the 1st or 8th rank
        #TO DO : decide whether to make it more general and recover pawns at the same time as kings
        pawns = {
            color: [piece for piece in pieces.values() if isinstance(piece, Pawn)]
            for color, pieces in self.pieces.items()
        }
        for pawn_list in pawns.values():
            for pawn in pawn_list:
                if pawn.current_square.row in [0,7]:
                    raise exceptions.PawnOnFirstOrEighthRowError(pawn)

    def is_valid_position(self):
        try:
            self.assert_valid_position()
        except exceptions.InvalidPositionError as e:
            print (e)
            return False
        else:
            return True


#Succession of positions
class Game:
    def __init__(self):
        self.positions = []
        pass

    def add_position(self, position: Position):
        self.positions.append(position)

    def get_position(self, halfmove_number: int):
        return self.positions[halfmove_number]