from __future__ import annotations

from .square import Square
from .pieces import Piece
from . import utils
from typing import Optional


# TO DO : For now board and position are intertwined, that will need some refacto once considering historics
class Board:
    def __init__(self, empty=False):
        self.columns, self.rows = utils.generate_columns_rows()
        self._create_squares()
        self.pieces = self.pieces_initialize()  # keys : [color] [piece_type]
        if not empty:
            self._initial_position()

    @staticmethod
    def pieces_initialize() -> dict[str, dict[str, set[Piece]]]:
        colors = ["white", "black"]
        piece_types = ["King", "Queen", "Rook", "Bishop", "Knight", "Pawn"]

        pieces = {}
        for color in colors:
            pieces[color] = {}
            for piece_type in piece_types:
                pieces[color][piece_type] = set()
        return pieces

    def __str__(self):
        board_string = " ——" * 8 + "\n"
        for row in reversed(self.rows):
            board_string += "|"
            for column in self.columns:
                board_string += str(self.square(column + row)) + "|"
            board_string += "\n" + " ——" * 8 + "\n"
        return board_string

    def square(self, key) -> Optional["Square"]:
        # Returns None if the label or indices point at a square not in the grid.
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
        all_pieces = set()
        for type_dict in self.pieces.values():
            for piece_set in type_dict.values():
                for piece in piece_set:
                    all_pieces.add(piece)
        return all_pieces


if __name__ == "__main__":
    pass
