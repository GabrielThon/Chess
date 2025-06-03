import pytest
from src.models.exceptions import InvalidColorError, UnimplementedPieceTypeError
from src.models.directions import Direction


def test_place_valid(emptyboard):
    square = emptyboard.square("a2")
    assert not square.piece
    pawn = square.place("white", "Pawn")
    assert pawn is not None
    assert square.piece == pawn
    assert pawn.current_square == square
    assert pawn in square.board.pieces["white"]["Pawn"]


def test_place_invalid_inputs(emptyboard):
    square = emptyboard.square("a2")
    with pytest.raises(InvalidColorError):
        square.place("red", "Pawn")
    with pytest.raises(UnimplementedPieceTypeError):
        square.place("white", "InvalidPieceType")


def test_remove_piece(emptyboard):
    square = emptyboard.square("a2")
    pawn = square.place("white", "Pawn")
    square.remove_piece()
    assert square.piece is None
    assert pawn.current_square is None
    assert not square.board.pieces["white"]["Pawn"]


def test_next_square_in_direction(emptyboard):
    square_a2 = emptyboard.square("a2")
    assert square_a2.next_square_in_direction(Direction(1, 0)).name == "b2"
    assert square_a2.next_square_in_direction(Direction(0, 1)).name == "a3"
    assert square_a2.next_square_in_direction(Direction(0, -1)).name == "a1"
    assert square_a2.next_square_in_direction(Direction(-1, 0)) is None


def test_explore_in_direction_blocking_piece(emptyboard):
    square_a2 = emptyboard.square("a2")
    pawn_d2 = emptyboard.square("d2").place("white", "Pawn")
    assert square_a2.explore_in_direction(Direction(1, 0)) == ({emptyboard.square("b2"), emptyboard.square("c2"), emptyboard.square("d2")}, pawn_d2)

def test_explore_in_direction_board_edge(emptyboard):
    square_a2 = emptyboard.square("d2")
    assert square_a2.explore_in_direction(Direction(-1, 0)) == ({emptyboard.square("a2"), emptyboard.square("b2"), emptyboard.square("c2")}, None)
