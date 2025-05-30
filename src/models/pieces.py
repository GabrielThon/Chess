from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional

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
    def controlled_squares(self) -> set[Square]:
        pass

    def moving_squares(self) -> set[Square]:  # Applies to all pieces except Pawn and King where it is overloaded
        return {
            square for square in self.controlled_squares()
            if not square.piece or square.piece.color == self.opposite_color
        }

    @abstractmethod
    def moving_directions(self) -> list:
        pass

    @property
    def is_pinned(self) -> [bool, tuple[int,int]]:
        return [False, None]


class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Pawn")
        self.starting_row = 1 if self.color == "white" else 6
        # self.en_passant_row = 4 if self.color == "white" else 3
        # self.moved_two_squares_forward = False

    def controlled_squares(self) -> set[Square]:
        defended_squares = set()
        directions = self.capturing_directions()

        for direction in directions:
            square = self.current_square.next_square_in_direction(direction)
            if square:
                defended_squares.add(square)
        return defended_squares

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
        defended_squares = set()
        directions = self.moving_directions()
        for direction in directions:
            square = self.current_square.next_square_in_direction(direction)
            if square:
                defended_squares.add(square)
        return defended_squares

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


class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Bishop")

    def controlled_squares(self) -> set[Square]:
        defended_squares = set()
        directions = self.moving_directions()
        for direction in directions:
            while True:
                square = self.current_square.next_square_in_direction(direction)
                if not square:
                    break
                elif square.piece:
                    defended_squares.add(square)
                    break
        return defended_squares

    def moving_directions(self) -> list[tuple[int, int]]:
        return [(1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1)
                ]


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Rook")

    def controlled_squares(self) -> set[Square]:
        defended_squares = set()
        directions = self.moving_directions()
        for direction in directions:
            while True:
                square = self.current_square.next_square_in_direction(direction)
                if not square:
                    break
                elif square.piece:
                    defended_squares.add(square)
                    break
        return defended_squares

    def moving_directions(self) -> list[tuple[int, int]]:
        return [(0, 1),
                (0, -1),
                (1, 0),
                (-1, 0)
                ]


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Queen")

    def controlled_squares(self) -> set[Square]:
        defended_squares = set()
        directions = self.moving_directions()
        for direction in directions:
            while True:
                square = self.current_square.next_square_in_direction(direction)
                if not square:
                    break
                elif square.piece:
                    defended_squares.add(square)
                    break
        return defended_squares

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
        defended_squares = set()
        directions = self.moving_directions()
        for direction in directions:
            while True:
                square = self.current_square.next_square_in_direction(direction)
                if not square:
                    break
                elif square.piece:
                    defended_squares.add(square)
                    break
        return defended_squares

    def moving_squares(self) -> set[Square]:
        moving_squares = set()
        board = self.current_square.board
        opposite_color_pieces = board.black_pieces if self.color == "white" else board.white_pieces
        for square in self.controlled_squares():
            if not square.piece or square.piece.color == self.opposite_color:
                for piece in opposite_color_pieces.values():
                    if square in piece.controlled_squares():
                        break
                else:
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
