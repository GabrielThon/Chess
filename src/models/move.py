from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pieces import Piece
    from .square import Square
    from.position import Position


class Move:
    def __init__(self, position: "Position", piece: "Piece", square: "Square", *, is_castling = False, rook_start = None, rook_end = None, is_two_pawn_move = False, is_en_passant = False):
        self.former_position = position
        self.piece = piece
        self.start_square = piece.square
        self.end_square = square
        self.is_castling = is_castling
        self.rook_start = rook_start
        self.rook_end = rook_end
        self.is_two_pawn_move = is_two_pawn_move
        self.is_en_passant = is_en_passant


    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (
                self.former_position is other.former_position and
                self.piece is other.piece and
                self.start_square is other.start_square and
                self.end_square is other.end_square and
                self.is_castling == other.is_castling
        )

    def __hash__(self):
        return hash((
            self.former_position,
            self.piece,
            self.start_square,
            self.end_square,
        ))

    def is_legal_move(self):
        if not self.former_position.legal_moves_:
            self.former_position.compute_legal_moves()
        return self in self.former_position.legal_moves_.get(self.piece, set())
