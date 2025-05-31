from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.pieces import Pawn


class OutofBoundSquareError(Exception):
    """Exception raised when a square is not within the board"""

    def __init__(self, key):
        super().__init__(f"Square '{key}' is out of bounds.")
        self.key = key


class InvalidPositionError(Exception):
    """Base class for invalid position errors"""
    pass


class InvalidNumberOfKingsError(InvalidPositionError):
    """Raised when the position doesn't contain 1 king of each color"""

    def __init__(self):
        super().__init__(
            f"Invalid position: must have exactly one king of each color.")


class NonPlayingPlayerKingInCheckError(InvalidPositionError):
    """Raised when the position doesn't contain 1 king of each color"""

    def __init__(self, color: str):
        super().__init__(f"Invalid position: {color}'s king is in check but it is not their turn to move.")


class PawnOnFirstOrEighthRowError(InvalidPositionError):
    """Raised on first encounter of a pawn on first or eighth row"""

    def __init__(self, pawn: "Pawn"):
        super().__init__(f"Invalid position : Pawn on {pawn.current_square.name} cannot be there")
