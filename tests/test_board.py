import pytest

from chess.models.square import Square
from chess.models import utils


def test_square_with_invalid_strings(emptyboard):
    invalid_string_squares = ["randomstring",
                              "a0",
                              "a9",
                              "i2"]
    for string in invalid_string_squares:
        with pytest.raises(ValueError):
            Square(string, emptyboard)
        assert emptyboard.square(string) is None

def test_board_place(emptyboard):
    assert not emptyboard.square("a2").piece
    pawna2 = emptyboard.place_piece("white","Pawn","a2")
    assert pawna2 in emptyboard.pieces["white"]["Pawn"]

def test_initial_position(starting_position):
    # There should be 16 pieces of each color
    assert sum(len(piece_types) for piece_types in starting_position.pieces["white"].values())== 16
    assert sum(len(piece_types) for piece_types in starting_position.pieces["black"].values())== 16

    # Checking pieces types and color on all squares matching starting position
    for [color, piece_type, square_label] in utils.starting_position():
        square = starting_position.square(square_label)
        piece = square.piece
        assert piece.type == piece_type
        assert piece.color == color

def test_board_remove(starting_position):
    assert starting_position.square("a2").piece
    starting_position.remove_piece("a2")
    assert not starting_position.square("a2").piece