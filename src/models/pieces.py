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
        return f"{self.color.capitalize()} {self.type} on {self.current_square.name}"

    def __str__(self):
        return f"{self.color.capitalize()} {self.type} on {self.current_square.name}"

    @abstractmethod
    def controlled_squares(self) -> set[Square]:
        pass

    def moving_squares(self) -> set[Square]:  # Applies to all pieces except Pawn and King where it is overloaded
        return {
            square for square in self.controlled_squares()
            if not square.piece or square.piece.color == self.opposite_color
        }

    @abstractmethod
    def moving_directions(self) -> list[tuple[int, int]]:
        pass


class RecursiveControlledSquaresMixin:
    # Inheriting classes must implement attribute current_square and method moving_directions
    def controlled_squares(self) -> set[Square]:
        controlled_squares: set["Square"] = set()
        directions = self.moving_directions()
        for direction in directions:
            controlled_squares = controlled_squares | self.current_square.explore_in_direction(direction)[0]
        return controlled_squares


class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Pawn")
        self.starting_row = 1 if self.color == "white" else 6
        # self.en_passant_row = 4 if self.color == "white" else 3
        # self.moved_two_squares_forward = False

    def controlled_squares(self) -> set[Square]:
        controlled_squares = set()
        directions = self.capturing_directions()

        for direction in directions:
            square = self.current_square.next_square_in_direction(direction)
            if square:
                controlled_squares.add(square)
        return controlled_squares

    def moving_squares(self) -> set[Square]:
        # TO DO : prise en passant. Required : move and last_piece to move
        column, row = utils.label_to_indices(self.current_square.name)
        moving_squares = set()
        directions = self.moving_directions()

        # Checking moving forward
        square = self.current_square.next_square_in_direction(directions[0])
        if square and not square.piece:
            moving_squares.add(square)
            if row == self.starting_row:  # If the pawn is on its starting square, check if it can moves two moving_squares ahead
                square = square.next_square_in_direction(directions[0])
                if square and not square.piece:
                    moving_squares.add(square)
        # Checking captures
        for square in self.controlled_squares():
            if square.piece and square.piece.color == self.opposite_color:
                moving_squares.add(square)
        return moving_squares

    def moving_directions(self) -> list[tuple[int, int]]:
        moving_direction = 1 if self.color == "white" else -1
        return [(0, moving_direction)]

    def capturing_directions(self) -> list[tuple[int, int]]:
        moving_direction = 1 if self.color == "white" else -1
        return [(1, moving_direction),
                (-1, moving_direction)]


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Knight")

    def controlled_squares(self) -> set[Square]:
        controlled_squares = set()
        directions = self.moving_directions()
        for direction in directions:
            square = self.current_square.next_square_in_direction(direction)
            if square:
                controlled_squares.add(square)
        return controlled_squares

    def moving_directions(self) -> list[tuple[int, int]]:
        return [(1, 2),
                (2, 1),
                (2, -1),
                (1, -2),
                (-1, -2),
                (-2, -1),
                (-2, 1),
                (-1, 2)
                ]


class Bishop(RecursiveControlledSquaresMixin, Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Bishop")

    def moving_directions(self) -> list[tuple[int, int]]:
        return [(1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1)
                ]


class Rook(RecursiveControlledSquaresMixin, Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Rook")

    def moving_directions(self) -> list[tuple[int, int]]:
        return [(0, 1),
                (0, -1),
                (1, 0),
                (-1, 0)
                ]


class Queen(RecursiveControlledSquaresMixin, Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Queen")

    def moving_directions(self) -> list[tuple[int, int]]:
        return [(1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0)
                ]


class King(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "King")

    def controlled_squares(self) -> set[Square]:
        controlled_squares = set()
        directions = self.moving_directions()
        for direction in directions:
            square = self.current_square.next_square_in_direction(direction)
            if square:
                controlled_squares.add(square)
        return controlled_squares

    def moving_squares(self) -> set[Square]:
        moving_squares = set()
        board = self.current_square.board
        for square in self.controlled_squares():
            if not square.piece or square.piece.color != self.color:
                moving_squares.add(square)
        return moving_squares

    def moving_directions(self) -> list[tuple[int, int]]:
        return [(1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0)
                ]
