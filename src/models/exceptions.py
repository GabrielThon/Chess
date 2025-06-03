from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.pieces import Pawn


class OutofBoundSquareError(Exception):
    """Exception raised when a square is not within the board"""

    def __init__(self, key):
        super().__init__(f"Square '{key}' is out of bounds.")


class InvalidColorError(Exception):
    """Exception raised if a wrong color argument is passed to a function. Valid colors are white and black (insensitive to case)"""

    def __init__(self, color):
        super().__init__(f"Color must be white or black but {color} was given")


class UnimplementedPieceTypeError(Exception):
    """Exception raised if a wrong color argument is passed to a function. Valid colors are white and black (insensitive to case)"""

    def __init__(self, type):
        super().__init__(f"Class {type} is not currently implemented")

class InvalidPositionError(Exception):
    """Base class for invalid position errors"""
    pass


class InvalidNumberOfKingsError(InvalidPositionError):
    """Raised when the position doesn't contain 1 king of each color"""

    def __init__(self):
        super().__init__(f"Invalid position: must have exactly one king of each color.")


class NonPlayingPlayerKingInCheckError(InvalidPositionError):
    """Raised when the position doesn't contain 1 king of each color"""

    def __init__(self, color: str):
        super().__init__(f"Invalid position: {color}'s king is in check but it is not their turn to move.")


class PawnOnFirstOrEighthRowError(InvalidPositionError):
    """Raised on first encounter of a pawn on first or eighth row"""

    def __init__(self):
        super().__init__(f"Invalid position : A pawn is on the first or eighth rank")
