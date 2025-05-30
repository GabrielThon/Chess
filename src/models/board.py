from __future__ import annotations

from .pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from . import utils
from .exceptions import InvalidNumberOfKingsError
from typing import Optional

#TO DO : For now board and position are intertwined, that will need some refacto once considering historics
class Board:
    def __init__(self):
        self.columns, self.rows = utils.generate_columns_rows()
        self._create_squares()
        self.pieces: dict[str, dict[str,Piece]] = {}
        self._initial_position()

    @classmethod
    def create_empty_board(cls):
        board = cls.__new__(cls)
        board.columns, board.rows = utils.generate_columns_rows()
        board._create_squares()
        board.white_pieces, board.black_pieces = {}, {}
        return board

    def __str__(self):
        board_string = " ——" * 8 + "\n"
        for row in reversed(self.rows):
            board_string += "|"
            for column in self.columns:
                board_string += str(self.square(column + row)) + "|"
            board_string += "\n" + " ——" * 8 + "\n"
        return board_string

    def square(self, key) -> Optional[Square]:
        #Returns None if the label or indices point at a square not in the grid.
        if isinstance(key, str):
            if not utils.is_valid_square_string(key):
                return None
            col_idx, row_idx = utils.label_to_indices(key)
        elif isinstance(key, (list, tuple)) and len(key) == 2:
            col_idx, row_idx = key
            if not (0 <= col_idx < 8 and 0 <= row_idx < 8):
                return None
        else:
            raise TypeError("Argument must be a string, list or tuple")

        return self.grid[col_idx][row_idx]

    def piece(self, key) -> Optional[Piece]:
        square = self.square(key)
        return square.piece if square else None

    def _create_squares(self):
        self.grid = [[Square(column + row, self) for row in self.rows] for column in self.columns]

    def _initial_position(self):
        for [color, piece, square] in utils.starting_position():
            self.place(color, piece, square)

    def place(self, color_string, piece_string, square_string) -> Optional[Piece]:
        return self.square(square_string).place(color_string, piece_string)

    def remove_piece(self, square_string):
        return self.square(square_string).remove_piece()

    @property
    def all_pieces(self):
        return {piece for color_pieces in self.pieces.values() for piece in color_pieces.values()}

    def controlled_squares(self, color_string: str) -> set[Square]:
        squares = set()
        pieces = self.pieces[color_string]
        for piece in pieces.values():
            squares = squares | piece.controlled_squares()
        return squares

#State of the board
class Position:
    def __init__(self, board: Board, whose_move: str):
        self.pieces = dict.copy(board.pieces)
        self.controlled_squares = {"white" : board.controlled_squares("white"),
                                   "black" : board.controlled_squares("black")}
        self.whose_move = whose_move

    def assert_valid_position(self):
        #Must have a single king of each color
        kings = {
            color: [piece for piece in pieces.values() if isinstance(piece, King)]
            for color, pieces in self.pieces.items()
        }
        nb_kings = {"white" :len(kings["white"]),
                    "black" :len(kings["white"])}
        for nb_king in nb_kings.values():
            if nb_king != 1:
                raise InvalidNumberOfKingsError(nb_kings)

        #The king of the player not playing must not be in check

    def is_valid_position(self):
        try:
            self.assert_valid_position()
        except InvalidNumberOfKingsError as e1:
            print (e1)
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

class Square:
    def __init__(self, string_square: str, board: Board):
        if not utils.is_valid_square_string(string_square):
            raise ValueError(f"Invalid square label: {string_square}")
        self.column,self.row = utils.label_to_indices(string_square)
        self.name = string_square
        self.board = board
        self.piece = None

    def __str__(self):
        if self.piece:
            return str(self.piece)
        else:
            return "  "


    def __repr__(self):
        return self.name

    def place(self, color_string, piece_string) -> Optional[Piece]:
        piece_string_to_cls = {
            "Pawn": Pawn,
            "Knight": Knight,
            "Bishop": Bishop,
            "Rook": Rook,
            "Queen": Queen,
            "King": King
        }
        piece_cls = piece_string_to_cls.get(piece_string)
        if piece_cls is None:
            return None

        piece = piece_cls(color=color_string)
        piece.current_square = self
        self.board.pieces[color_string][self.name] = piece
        return piece

    def remove_piece(self):
        # Returns false if no piece is found on the square
        if not self.piece:
            return False
        # Removes piece from the board corresponding color piece collection
        del self.board.pieces[self.piece.color][self.name]
        #Removes link between piece and square
        self.piece.current_square = None
        self.piece = None
        return True

    def next_square_in_direction(self, direction: tuple[int, int]) -> Square:
        return self.board.square([self.column + direction[0], self.row + direction[1]])


if __name__ == "__main__":
    pass
