from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pieces import Piece
    from .square import Square


class Move:
    def __init__(self, position: "Position", piece: "Piece", square: "Square"):
        self.former_position = position
        self.piece = piece
        self.departure_square = piece.square
        self.target_square = square

    def is_legal_move(self):
        if not self.former_position.legal_moves_:
            self.former_position.compute_legal_moves()
        return self.target_square in self.former_position.legal_moves_.get(self.piece, set())
