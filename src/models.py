from __future__ import annotations
import utils
from typing import Optional
from abc import ABC, abstractmethod


class Board:
    def __init__(self, with_squares=True, initial_position=True):
        self.columns, self.rows = utils.generate_columns_rows()
        self.white_pieces, self.black_pieces = [], []
        if with_squares:
            self._create_squares()
            if initial_position:
                self._initial_position()

    def __str__(self):
        board_string = " ——" * 8 + "\n"
        for row in reversed(self.rows):
            board_string += "|"
            for column in self.columns:
                board_string += str(self.square(column + row)) + "|"
            board_string += "\n" + " ——" * 8 + "\n"
        return board_string

    def square(self, key) -> Optional[Square]:
        if isinstance(key, str):
            col, row = utils.label_to_indices(key)
        elif isinstance(key, list) and len(key) == 2:
            col, row = key[0], key[1]
        else:
            raise ValueError("Argument must be a square label (ex : 'a5') or indices (ex : [0, 4])")
        if 0 <= col < 8 and 0 <= row < 8:
            return self.grid[col][row]
        else:
            return None

    def piece(self, key) -> Optional[Piece]:
        square = self.square(key)
        return square.piece if square else None

    def _create_squares(self):
        self.grid = [[Square(column + row, self) for row in self.rows] for column in self.columns]

    def _initial_position(self):
        for [color, piece, square] in utils.starting_position():
            self.place(color, piece, square)

    def place(self, color_string, piece_string, square_string):
        return self.square(square_string).place(color_string, piece_string)

    def remove_piece(self, square_string):
        return self.square(square_string).remove_piece()

    @property
    def occupied_squares(self):
        return [self.square(col + row) for col in self.columns for row in self.rows if self.square(col + row).piece]


class Square:
    def __init__(self, string_square: str, board: Board = None):
        if not utils.is_valid_square_string(string_square):
            raise ValueError(f"Wrong argument in the Square constructor : {string_square}")
        self.column,self.row = utils.label_to_indices(string_square)
        self.name = string_square[0] + string_square[1]
        self.board = board
        self.piece = None

    def __str__(self):
        if self.piece:
            return str(self.piece)
        else:
            return "  "


    def __repr__(self):
        return self.name

    def place(self, color_string, piece_string):
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
            return False

        piece_cls(color_string).place_on_square(self)
        return True

    def remove_piece(self):
        if self.piece:
            self.piece = None
            return True
        return False


class Piece(ABC):
    def __init__(self, color: str, type: str):
        if not utils.is_valid_color(color):
            raise ValueError("Wrong color specified for the piece : ", color)
        self.color = color.lower()
        self.opposite_color = "black" if self.color == "white" else "white"
        self.type = type
        self.current_square = None

    def __repr__(self):
        return f"{self.type[0]}{self.current_square}-{self.color[0]}"

    def __str__(self):
        return self.type[0] + self.color[0]

    def place_on_square(self, square: Square):
        self.current_square = square
        square.piece = self
        if square.board:
            if self.color == "white":
                square.board.white_pieces.append([str(self),repr(square)])
            else:
                square.board.black_pieces.append([str(self),repr(square)])

    @abstractmethod
    def defended_squares(self) -> list[Square]:
        pass

    def moving_squares(self) -> list[Square]:  # Applies to all pieces except Pawn and King where it is overloaded
        return [square for square in self.defended_squares() if
                (not square.piece or square.piece.color == self.opposite_color)]


class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Pawn")
        self.moving_direction = 1 if self.color == "white" else -1
        self.starting_row = 1 if self.color == "white" else 6
        # self.en_passant_row = 4 if self.color == "white" else 3
        # self.moved_two_squares_forward = False

    def defended_squares(self) -> list[Square]:
        column, row = utils.label_to_indices(self.current_square.name)
        board = self.current_square.board
        defended_squares = []
        square = board[[column - 1, row + self.moving_direction]]
        if square:
            defended_squares.append(square)
        square = board[[column + 1, row + self.moving_direction]]
        if square:
            defended_squares.append(square)
        return defended_squares

    def moving_squares(self) -> list[Square]:
        # TO DO : prise en passant. Required : move and last_piece to move
        column, row = utils.label_to_indices(self.current_square.name)
        board = self.current_square.board
        moving_squares = []

        # Checking moving forward
        square = board[[column, row + self.moving_direction]]
        if square and not square.piece:
            moving_squares.append(square)
            if row == self.starting_row:  # If the pawn is on its starting square, check if it can moves two moving_squares ahead
                square = board[[column, row + 2 * self.moving_direction]]
                if square and not square.piece:
                    moving_squares.append(square)
        # Checking captures
        for square in self.defended_squares():
            if square.piece and square.piece.color == self.opposite_color:
                moving_squares.append(square)
        return moving_squares


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Knight")

    def defended_squares(self) -> list[Square]:
        defended_squares = []
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
            square_to_examine = board[[examined_column, examined_row]]
            if square_to_examine:
                defended_squares.append(square_to_examine)
        return defended_squares


class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Bishop")

    def defended_squares(self) -> list[Square]:
        board = self.current_square.board
        directions = [[1, 1],
                      [1, -1],
                      [-1, 1],
                      [-1, -1],
                      ]
        defended_squares = []
        current_column, current_row = utils.label_to_indices(self.current_square.name)
        for direction in directions:
            examined_column, examined_row = current_column, current_row
            while True:
                examined_column, examined_row = examined_column + direction[0], examined_row + direction[1]
                square_to_examine = board[[examined_column, examined_row]]
                if not square_to_examine:
                    break
                if square_to_examine.piece:
                    defended_squares.append(square_to_examine)
                    break
        return defended_squares


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Rook")

    def defended_squares(self) -> list[Square]:
        board = self.current_square.board
        directions = [[0, 1],
                      [0, -1],
                      [1, 0],
                      [-1, 0],
                      ]
        defended_squares = []
        current_column, current_row = utils.label_to_indices(self.current_square.name)
        for direction in directions:
            examined_column, examined_row = current_column, current_row
            while True:
                examined_column, examined_row = examined_column + direction[0], examined_row + direction[1]
                square_to_examine = board[[examined_column, examined_row]]
                if not square_to_examine:
                    break
                if square_to_examine.piece:
                    defended_squares.append(square_to_examine)
                    break
        return defended_squares


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "Queen")

    def defended_squares(self) -> list[Square]:
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
        defended_squares = []
        current_column, current_row = utils.label_to_indices(self.current_square.name)
        for direction in directions:
            examined_column, examined_row = current_column, current_row
            while True:
                examined_column, examined_row = examined_column + direction[0], examined_row + direction[1]
                square_to_examine = board[[examined_column, examined_row]]
                if not square_to_examine:
                    break
                if square_to_examine.piece:
                    defended_squares.append(square_to_examine)
                    break
        return defended_squares


class King(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower(), "King")

    def defended_squares(self) -> list[Square]:
        defended_squares = []
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
            square_to_examine = board[[examined_column, examined_row]]
            if square_to_examine:
                defended_squares.append(square_to_examine)
        return defended_squares

    def moving_squares(self) -> list[Square]:
        moving_squares = []
        board = self.current_square.board
        opposite_color_pieces = board.black_pieces if self.color == "white" else board.white_pieces
        for square_to_examine in self.defended_squares():
            if not square_to_examine.piece or square_to_examine.piece.color == self.opposite_color:
                for piece in opposite_color_pieces:
                    if square_to_examine in piece.defended_squares():
                        break
                else:
                    moving_squares.append(square_to_examine)
        return moving_squares


if __name__ == "__main__":
    chessboard = Board()
    print(chessboard)
