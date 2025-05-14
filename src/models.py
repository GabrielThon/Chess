import utils
from typing import List

COLUMNS = ['a','b','c','d','e','f','g','h']
ROWS = ['1','2','3','4','5','6','7','8']

class Board:
    def __init__(self):
        self.create_squares()
        self.initial_position()

    def create_squares(self):
        self.squares = {}
        for i,column in enumerate(COLUMNS):
            for j,row in enumerate(ROWS):
                self.squares[column+row] = Square(column+row,self)

    def initial_position(self):
        Rook("white").place_on_square(self.squares["a1"])
        Rook("white").place_on_square(self.squares["h1"])
        Knight("white").place_on_square(self.squares["b1"])
        Knight("white").place_on_square(self.squares["g1"])
        Bishop("white").place_on_square(self.squares["c1"])
        Bishop("white").place_on_square(self.squares["f1"])
        Queen("white").place_on_square(self.squares["d1"])
        King("white").place_on_square(self.squares["e1"])

        Rook("black").place_on_square(self.squares["a8"])
        Rook("black").place_on_square(self.squares["h8"])
        Knight("black").place_on_square(self.squares["b8"])
        Knight("black").place_on_square(self.squares["g8"])
        Bishop("black").place_on_square(self.squares["c8"])
        Bishop("black").place_on_square(self.squares["f8"])
        Queen("black").place_on_square(self.squares["d8"])
        King("black").place_on_square(self.squares["e8"])

        for column in COLUMNS:
            Pawn("white").place_on_square(self.squares[column + "2"])
            Pawn("black").place_on_square(self.squares[column + "7"])

    def __str__(self):
        board_string = " ——" * 8 + "\n"
        for row in reversed(ROWS):
            board_string += "|"
            for column in COLUMNS:
                board_string += self.squares[column+row].display + "|"
            board_string += "\n" + " ——" * 8 + "\n"
        return board_string

class Square:
    def __init__(self, string_square : str, board : Board):
        if not utils.is_valid_string_square(string_square):
            raise ValueError("Wrong argument in the Square constructor : ", string_square)
        self.row = string_square[0]
        self.column = string_square[1]
        self.name = string_square[0] + string_square[1]
        self.board = board
        self.occupying_piece = None

    @property
    def display(self):
        if self.occupying_piece:
            return self.occupying_piece.display
        else:
            return "  "

class Piece:
    def __init__(self, color : str):
        self.current_square = None
        if not utils.is_valid_color(color):
            raise ValueError("Wrong color specified for the piece : ", color)
        self.color = color.lower()
        self.type = "Undefined"

    @property
    def display(self):
        return self.type[0]+self.color[0]

    def place_on_square(self, square : Square):
        self.current_square = square
        square.occupying_piece = self

    def possible_moves(self) -> List[Square]:
        pass

class Pawn(Piece):
    def __init__(self, color : str):
        super().__init__(color.lower())
        self.type = "Pawn"

    def possible_squares(self) -> List[Square]:
        squares = []
        current_column = self.current_square.column
        current_row = self.current_square.row
        if self.color == "white":
            front_square = self.current_square.board.squares[current_column+current_row]

        return squares


class Knight(Piece):
    def __init__(self, color : str):
        super().__init__(color.lower())
        self.type = "Knight"

class Bishop(Piece):
    def __init__(self, color : str):
        super().__init__(color.lower())
        self.type = "Bishop"

class Rook(Piece):
    def __init__(self, color : str):
        super().__init__(color.lower())
        self.type = "Rook"

class Queen(Piece):
    def __init__(self, color : str):
        super().__init__(color.lower())
        self.type = "Queen"

class King(Piece):
    def __init__(self, color : str):
        super().__init__(color.lower())
        self.type = "King"


if __name__ == "__main__":
    # string_squares = ["a1",
    #                   "h8",
    #                   "randomstring",
    #                   "a0",
    #                   "a9",
    #                   "i2"]
    # for string_square in string_squares:
    #     try:
    #         new_square = Square(string_square)
    #     except ValueError as e:
    #         print(e)
    #     else:
    #         print("Square successfully created : ", string_square)

    board = Board()
    print(board)
