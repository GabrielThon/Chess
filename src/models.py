import utils
import string
from typing import List


class Board:
    def __init__(self, with_squares=True, initial_position=True):
        self.columns, self.rows = utils.generate_columns_rows()
        self.white_pieces, self.black_pieces = [], []
        if with_squares:
            self._create_squares()
            if initial_position:
                self._initial_position()

    def _create_squares(self):
        self.grid = [[Square(column + row, self) for row in self.rows] for column in self.columns]

    def __getitem__(self, key):
        if isinstance(key, str):
            col, row = utils.label_to_indices(key)
        elif isinstance(key, list) and len(key) == 2:
            col, row = key[0], key[1]
        else:
            raise KeyError("Key must be a square label (ex : 'a5') or indices (ex : [0, 4])")
        if 0 <= col < 8 and 0 <= row < 8:
            return self.grid[col][row]
        else:
            return None

    def _initial_position(self):
        Rook("white").place_on_square(self["a1"])
        Rook("white").place_on_square(self["h1"])
        Knight("white").place_on_square(self["b1"])
        Knight("white").place_on_square(self["g1"])
        Bishop("white").place_on_square(self["c1"])
        Bishop("white").place_on_square(self["f1"])
        Queen("white").place_on_square(self["d1"])
        King("white").place_on_square(self["e1"])

        Rook("black").place_on_square(self["a8"])
        Rook("black").place_on_square(self["h8"])
        Knight("black").place_on_square(self["b8"])
        Knight("black").place_on_square(self["g8"])
        Bishop("black").place_on_square(self["c8"])
        Bishop("black").place_on_square(self["f8"])
        Queen("black").place_on_square(self["d8"])
        King("black").place_on_square(self["e8"])

        for column in range(8):
            Pawn("white").place_on_square(self[[column, 1]])
            Pawn("black").place_on_square(self[[column, 6]])

    def __str__(self):
        board_string = " ——" * 8 + "\n"
        for row in reversed(self.rows):
            board_string += "|"
            for column in self.columns:
                board_string += self[column + row].display + "|"
            board_string += "\n" + " ——" * 8 + "\n"
        return board_string

    @property
    def occupied_squares(self):
        return [self[col + row] for col in self.columns for row in self.rows if not self[col + row].isempty]


class Square:
    def __init__(self, string_square: str, board: Board):
        if not utils.is_valid_string_square(string_square):
            raise ValueError(f"Wrong argument in the Square constructor : {string_square}")
        self.column = string_square[0]
        self.row = string_square[1]
        self.name = self.column + self.row
        self.board = board
        self.occupying_piece = None

    @property
    def isempty(self):
        return self.occupying_piece is None

    @property
    def display(self):
        if self.isempty:
            return "  "
        else:
            return self.occupying_piece.display

    def __repr__(self):
        return f"{self.column}{self.row}"


class Piece:
    def __init__(self, color: str):
        self.current_square = None
        if not utils.is_valid_color(color):
            raise ValueError("Wrong color specified for the piece : ", color)
        self.color = color.lower()
        self.opposite_color = "black" if self.color == "white" else "white"
        self.type = "Undefined"

    @property
    def display(self):
        return self.type[0] + self.color[0]

    def place_on_square(self, square: Square):
        self.current_square = square
        square.occupying_piece = self
        if self.color == "white":
            square.board.white_pieces.append(self)
        else:
            square.board.black_pieces.append(self)

    def defended_squares(self) -> List[Square]:
        pass

    def moving_squares(self) -> List[Square]: #Applies to all pieces except Pawn and King where it is overloaded
        return [square for square in self.defended_squares() if
                (square.isempty or square.occupying_piece.color == self.opposite_color)]

    def __repr__(self):
        return f"{self.type[0]}{self.current_square}-{self.color}"


class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower())
        self.type = "Pawn"
        self.moving_direction = 1 if self.color == "white" else -1
        self.starting_row = 1 if self.color == "white" else 6
        # self.en_passant_row = 4 if self.color == "white" else 3
        # self.moved_two_squares_forward = False

    def defended_squares(self) -> List[Square]:
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

    def moving_squares(self) -> List[Square]:
        # TO DO : prise en passant. Required : move and last_piece to move
        column, row = utils.label_to_indices(self.current_square.name)
        board = self.current_square.board
        moving_squares = []

        # Checking moving forward
        square = board[[column, row + self.moving_direction]]
        if square and square.isempty:
            moving_squares.append(square)
            if row == self.starting_row:  # If the pawn is on its starting square, check if it can moves two moving_squares ahead
                square = board[[column, row + 2 * self.moving_direction]]
                if square and square.isempty:
                    moving_squares.append(square)
        # Checking captures
        for square in self.defended_squares():
            if not square.isempty and square.occupying_piece.color == self.opposite_color:
                moving_squares.append(square)
        return moving_squares


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower())
        self.type = "Knight"

    def defended_squares(self) -> List[Square]:
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

class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower())
        self.type = "Bishop"

    def defended_squares(self) -> List[Square]:
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
                if not square_to_examine.isempty:
                    defended_squares.append(square_to_examine)
                    break
        return defended_squares

class Rook(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower())
        self.type = "Rook"

    def defended_squares(self) -> List[Square]:
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
                if not square_to_examine.isempty:
                    defended_squares.append(square_to_examine)
                    break
        return defended_squares


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower())
        self.type = "Queen"

    def defended_squares(self) -> List[Square]:
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
                if not square_to_examine.isempty:
                    defended_squares.append(square_to_examine)
                    break
        return defended_squares


class King(Piece):
    def __init__(self, color: str):
        super().__init__(color.lower())
        self.type = "King"

    def defended_squares(self) -> List[Square]:
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

    def moving_squares(self) -> List[Square]:
        moving_squares = []
        board = self.current_square.board
        opposite_color_pieces = board.black_pieces if self.color == "white" else board.white_pieces
        for square_to_examine in self.defended_squares():
            if square_to_examine.isempty or square_to_examine.occupying_piece.color == self.opposite_color:
                for piece in opposite_color_pieces:
                    if square_to_examine in piece.defended_squares():
                        break
                else:
                    moving_squares.append(square_to_examine)
        return moving_squares

if __name__ == "__main__":
    ##Pawn
    # chessboard = Board()
    # Pawn("white").place_on_square(chessboard["a2"])
    # Pawn("white").place_on_square(chessboard["b2"])
    # Pawn("black").place_on_square(chessboard["b3"])
    # Pawn("black").place_on_square(chessboard["c3"])
    # Pawn("black").place_on_square(chessboard["h3"])
    # print(chessboard)
    # cases = chessboard.occupied_squares
    # for case in cases :
    #     print(case.name, case.occupying_piece.display, case.occupying_piece.moving_squares())

    ## Knight
    # chessboard = Board(initial_position=False)
    # Knight("white").place_on_square(chessboard["a1"])
    # print(chessboard)
    # cases = chessboard.occupied_squares
    # for case in cases :
    #     print(case.name, case.occupying_piece.display, case.occupying_piece.moving_squares())

    ## Bishop
    # chessboard = Board(initial_position=False)
    # Bishop("white").place_on_square(chessboard["d5"])
    # Pawn("white").place_on_square(chessboard["b3"])
    # Pawn("black").place_on_square(chessboard["f7"])
    # print(chessboard)
    # cases = chessboard.occupied_squares
    # for case in cases:
    #     print(case.name, case.occupying_piece.display, case.occupying_piece.moving_squares())

    ## King 1

    chessboard = Board(initial_position=False)
    King("white").place_on_square(chessboard["e5"])
    Pawn("white").place_on_square(chessboard["d6"])
    Pawn("black").place_on_square(chessboard["e6"])
    # Knight("black").place_on_square(chessboard["f8"])
    King("black").place_on_square(chessboard["d7"])
    print(chessboard)
    cases = chessboard.occupied_squares
    for case in cases:
        print(case.name, case.occupying_piece.display, case.occupying_piece.moving_squares())
