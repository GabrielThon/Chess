from . import utils, exceptions, pieces
import inspect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .position import Position
    from .directions import Direction

class Square:
    def __init__(self, string_square: str, position: "Position"):
        if not utils.is_valid_square_string(string_square):
            raise ValueError(f"Invalid square label: {string_square}")
        self.column, self.row = utils.label_to_indices(string_square)
        self.name = string_square
        self.position = position
        self.piece = None

    def __str__(self):
        if self.piece:
            return str(self.piece)
        else:
            return "  "

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Square):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def place(self, color_string, piece_string) -> "pieces.Piece":
        piece_string_to_cls = {
            name: cls
            for name, cls in vars(pieces).items()
            if inspect.isclass(cls)
               and issubclass(cls, pieces.Piece)
               and not inspect.isabstract(cls)
        }
        piece_cls = piece_string_to_cls.get(piece_string)
        if not piece_cls:
            raise exceptions.UnimplementedPieceTypeError(piece_string)

        piece = piece_cls(color=color_string)
        piece.square = self
        self.piece = piece
        return piece

    def remove_piece(self):
        # Returns false if no piece is found on the square
        if not self.piece:
            return False
        piece = self.piece
        # Removes piece from the position corresponding color piece collection
        self.position.pieces[piece.color][piece.type].remove(piece)
        # Removes link between piece and square
        piece.square = None
        self.piece = None
        return True

    def next_square_in_direction(self, direction: "Direction") -> "Square":
        return self.position.square([self.column + direction.dcol, self.row + direction.drow])

    def explore_in_direction(self, direction: "Direction") -> tuple[set["Square"], "pieces.Piece"]:
        squares: set["Square"] = set()
        square = self.next_square_in_direction(direction)
        while square:
            squares.add(square)
            if square.piece:
                blocking_piece = square.piece
                break
            square = square.next_square_in_direction(direction)
        else:
            blocking_piece = None

        return squares, blocking_piece