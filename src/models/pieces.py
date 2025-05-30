from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from . import utils

if TYPE_CHECKING:
    from .board import Square


class Piece(ABC):
    def __init__(self, color: str, type: str, square: Square = None):
        if not utils.is_valid_color(color):
            raise ValueError("Wrong color specified for the piece : ", color)
        self.color = color.lower()
        self.opposite_color = "black" if self.color == "white" else "white"
        self.type = type
        self.current_square = square
        self.image_path = Path().resolve() / "images" / (self.type + "_" + self.color + ".svg")

    def __repr__(self):
        return f"{self.type[0]}{self.current_square}-{self.color[0]}"

    def __str__(self):
        return self.type[0] + self.color[0]

    @abstractmethod
    def defended_squares(self) -> set[Square]:
        pass

    def moving_squares(self) -> set[Square]:  # Applies to all pieces except Pawn and King where it is overloaded
        return {
            square for square in self.defended_squares()
            if not square.piece or square.piece.color == self.opposite_color
        }


class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Pawn")
        self.moving_direction = 1 if self.color == "white" else -1
        self.starting_row = 1 if self.color == "white" else 6
        # self.en_passant_row = 4 if self.color == "white" else 3
        # self.moved_two_squares_forward = False

    def defended_squares(self) -> set[Square]:
        column, row = utils.label_to_indices(self.current_square.name)
        board = self.current_square.board
        defended_squares = set()
        square = board.square([column - 1, row + self.moving_direction])
        if square:
            defended_squares.add(square)
        square = board.square([column + 1, row + self.moving_direction])
        if square:
            defended_squares.add(square)
        return defended_squares

    def moving_squares(self) -> set[Square]:
        # TO DO : prise en passant. Required : move and last_piece to move
        column, row = utils.label_to_indices(self.current_square.name)
        board = self.current_square.board
        moving_squares = set()

        # Checking moving forward
        square = board.square([column, row + self.moving_direction])
        if square and not square.piece:
            moving_squares.add(square)
            if row == self.starting_row:  # If the pawn is on its starting square, check if it can moves two moving_squares ahead
                square = board.square([column, row + 2 * self.moving_direction])
                if square and not square.piece:
                    moving_squares.add(square)
        # Checking captures
        for square in self.defended_squares():
            if square.piece and square.piece.color == self.opposite_color:
                moving_squares.add(square)
        return moving_squares


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Knight")

    def defended_squares(self) -> set[Square]:
        defended_squares = set()
        board = self.current_square.board
        directions = [[1, 2],
                      [2, 1],
                      [2, -1],
                      [1, -2],
                      [-1, -2],
                      [-2, -1],
                      [-2, 1],
                      [-1, 2],
                      ]
        for direction in directions:
            current_column, current_row = utils.label_to_indices(self.current_square.name)
            examined_column, examined_row = current_column + direction[0], current_row + direction[1]
            square_to_examine = board.square([examined_column, examined_row])
            if square_to_examine:
                defended_squares.add(square_to_examine)
        return defended_squares


class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Bishop")

    def defended_squares(self) -> set[Square]:
        board = self.current_square.board
        directions = [[1, 1],
                      [1, -1],
                      [-1, 1],
                      [-1, -1],
                      ]
        defended_squares = set()
        current_column, current_row = utils.label_to_indices(self.current_square.name)
        for direction in directions:
            examined_column, examined_row = current_column, current_row
            while True:
                examined_column, examined_row = examined_column + direction[0], examined_row + direction[1]
                square_to_examine = board.square([examined_column, examined_row])
                if not square_to_examine:
                    break
                if square_to_examine.piece:
                    defended_squares.add(square_to_examine)
                    break
        return defended_squares


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Rook")

    def defended_squares(self) -> set[Square]:
        board = self.current_square.board
        directions = [[0, 1],
                      [0, -1],
                      [1, 0],
                      [-1, 0],
                      ]
        defended_squares = set()
        current_column, current_row = utils.label_to_indices(self.current_square.name)
        for direction in directions:
            examined_column, examined_row = current_column, current_row
            while True:
                examined_column, examined_row = examined_column + direction[0], examined_row + direction[1]
                square_to_examine = board.square([examined_column, examined_row])
                if not square_to_examine:
                    break
                if square_to_examine.piece:
                    defended_squares.add(square_to_examine)
                    break
        return defended_squares


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Queen")

    def defended_squares(self) -> set[Square]:
        board = self.current_square.board
        directions = [[1, 1],
                      [1, -1],
                      [-1, 1],
                      [-1, -1],
                      [0, 1],
                      [0, -1],
                      [1, 0],
                      [-1, 0],
                      ]
        defended_squares = set()
        current_column, current_row = utils.label_to_indices(self.current_square.name)
        for direction in directions:
            examined_column, examined_row = current_column, current_row
            while True:
                examined_column, examined_row = examined_column + direction[0], examined_row + direction[1]
                square_to_examine = board.square([examined_column, examined_row])
                if not square_to_examine:
                    break
                if square_to_examine.piece:
                    defended_squares.add(square_to_examine)
                    break
        return defended_squares


class King(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "King")

    def defended_squares(self) -> set[Square]:
        defended_squares = set()
        board = self.current_square.board
        directions = [[1, 1],
                      [1, -1],
                      [-1, 1],
                      [-1, -1],
                      [0, 1],
                      [0, -1],
                      [1, 0],
                      [-1, 0],
                      ]
        for direction in directions:
            current_column, current_row = utils.label_to_indices(self.current_square.name)
            examined_column, examined_row = current_column + direction[0], current_row + direction[1]
            square_to_examine = board.square([examined_column, examined_row])
            if square_to_examine:
                defended_squares.add(square_to_examine)
        return defended_squares

    def moving_squares(self) -> set[Square]:
        moving_squares = set()
        board = self.current_square.board
        opposite_color_pieces = board.black_pieces if self.color == "white" else board.white_pieces
        for square_to_examine in self.defended_squares():
            if not square_to_examine.piece or square_to_examine.piece.color == self.opposite_color:
                for piece in opposite_color_pieces.values():
                    if square_to_examine in piece.defended_squares():
                        break
                else:
                    moving_squares.add(square_to_examine)
        return moving_squares
