import pytest

from src.models.exceptions import InvalidColorError, UnimplementedPieceTypeError
from src.models.directions import Direction
from src.models.position import Position


def test_place_valid():
    position = Position([])
    square = position.square("a2")
    assert not square.piece
    pawn = position.place_piece("white", "Pawn", "a2")
    assert pawn is not None
    assert square.piece == pawn
    assert pawn.square == square
    assert pawn in position.pieces["white"]["Pawn"]


def test_place_invalid_inputs():
    position = Position([])
    with pytest.raises(InvalidColorError):
        position.place_piece("red", "Pawn", "a2")
    with pytest.raises(UnimplementedPieceTypeError):
        position.place_piece("white", "InvalidPieceType", "a2")


def test_remove_piece():
    position = Position([])
    square = position.square("a2")
    pawn = position.place_piece("white", "Pawn", "a2")
    position.remove_piece("a2")
    assert square.piece is None
    assert pawn.square is None
    assert not position.pieces["white"]["Pawn"]


def test_next_square_in_direction():
    position = Position([])
    square_a2 = position.square("a2")
    assert square_a2.next_square_in_direction(Direction(1, 0)) == position.square("b2")
    assert square_a2.next_square_in_direction(Direction(0, 1)) == position.square("a3")
    assert square_a2.next_square_in_direction(Direction(0, -1)) == position.square("a1")
    assert square_a2.next_square_in_direction(Direction(-1, 0)) is None


def test_explore_in_direction_blocking_piece():
    position = Position([])
    square_a2 = position.square("a2")
    pawn_d2 = position.square("d2").place("white", "Pawn")
    assert square_a2.explore_in_direction(Direction(1, 0)) == ({position.square("b2"), position.square("c2"), position.square("d2")}, pawn_d2)


def test_explore_in_direction_board_edge():
    position = Position([])
    square_a2 = position.square("d2")
    assert square_a2.explore_in_direction(Direction(-1, 0)) == ({position.square("a2"), position.square("b2"), position.square("c2")}, None)
