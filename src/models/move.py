from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pieces import Piece
    from .square import Square
    from .position import Position


class Move:
    def __init__(self, position: "Position", piece: "Piece", square: "Square", *, is_castling = False, rook_start = None, rook_end = None, is_two_pawn_move = False, is_en_passant = False, is_promotion = False, promoting_piece_str = None):
        self.former_position = position
        self.piece = piece
        self.start_square = piece.square
        self.end_square = square
        self.is_castling = is_castling
        self.rook_start = rook_start
        self.rook_end = rook_end
        self.is_two_pawn_move = is_two_pawn_move
        self.is_en_passant = is_en_passant
        self.is_promotion = is_promotion
        self.promoting_piece_str = promoting_piece_str
        self.notation = None


    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (
                self.former_position is other.former_position and
                self.piece is other.piece and
                self.end_square is other.end_square and
                self.is_castling == other.is_castling and
                self.promoting_piece_str == other.promoting_piece_str
        )

    def __hash__(self):
        return hash((
            self.former_position,
            self.piece,
            self.start_square,
            self.end_square,
        ))

    def is_legal_move(self) -> bool:
        if not self.former_position.legal_moves_:
            self.former_position.compute_legal_moves()
        return self in self.former_position.legal_moves_.get(self.piece, set())

    def is_promotion(self) -> bool:
        return self.piece.type == "Pawn" and self.end_square.row in [0, 7]

    def is_capture(self) -> bool:
        #Assumes move is legal
        return (self.end_square.piece is not None) | self.is_en_passant

    def _multiple_pieces_notation(self):
        if self.piece.type == "Pawn":
            return ""
        if not self.former_position.legal_moves_:
            self.former_position.compute_legal_moves()
        conflicting_pieces = []
        notation = ""
        for piece in self.former_position.legal_moves_.keys():
            if piece != self.piece and piece.type == self.piece.type:
                for move in self.former_position.legal_moves_[piece]:
                    if move.end_square == self.end_square:
                        conflicting_pieces.append(piece)
        if not conflicting_pieces:
            return ""
        if not any(piece.square.column == self.piece.square.column for piece in conflicting_pieces):
            return self.piece.square.name[0]
        if not any(piece.square.row == self.piece.square.row for piece in conflicting_pieces):
            return self.piece.square.name[1]
        return self.piece.square.name[0] + self.piece.square.name[1]

    def _capture_notation(self):
        if self.piece.type == "Pawn":
            return self.piece.square.name[0] + "x"
        else:
            return "x"

    def compute_french_notation(self):
        if self.is_castling:
            if self.end_square.name in ["g1","g8"]:
                return "0-0"
            return "0-0-0"
        piece_cls_to_notation = {
            "Pawn" : "",
            "Knight": "C",
            "Bishop": "F",
            "Rook": "T",
            "Queen": "D",
            "King": "R"
        }
        piece_notation = piece_cls_to_notation[self.piece.__class__.__name__]
        target_square_notation = self.end_square.name
        capture_notation = self._capture_notation() if self.is_capture() else ""
        mutiple_piece_notation = self._multiple_pieces_notation()
        promotion_notation = "=" + piece_cls_to_notation[self.promoting_piece_str] if self.is_promotion else ""
        self.notation = piece_notation + mutiple_piece_notation + capture_notation + target_square_notation + promotion_notation

if __name__ == "__main__":
    from position import Position
    from utils import starting_position
    initial_position = Position(starting_position(),"white")
    start_square = initial_position.square_by_name["b1"]
    end_square = initial_position.square_by_name["c3"]
    move = Move(initial_position, start_square.piece, end_square)
    move.compute_french_notation()
    print(move.notation)