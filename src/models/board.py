from __future__ import annotations

from .pieces import *
from . import utils
from typing import Optional

class Board:
    def __init__(self):
        self.columns, self.rows = utils.generate_columns_rows()
        self._create_squares()
        self.white_pieces: dict[str,Piece] = {}
        self.black_pieces: dict[str,Piece] = {}
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
        return self.white_pieces | self.black_pieces

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
        self.piece = piece
        if color_string == "white":
            self.board.white_pieces[self.name] = piece
        else:
            self.board.black_pieces[self.name] = piece
        return piece

    def remove_piece(self):
        # Returns false if no piece is found on the square
        if not self.piece:
            return False
        # Removes piece from the board corresponding color piece collection
        if self.piece.color == "white":
            del self.board.white_pieces[self.name]
        else:
            del self.board.black_pieces[self.name]
        #Removes link between piece and square
        self.piece.current_square = None
        self.piece = None
        return True

    def next_square_in_direction(self, direction: tuple[int, int]) -> Square:
        return self.board.square([self.column + direction[0], self.row + direction[1]])


if __name__ == "__main__":
    pass
