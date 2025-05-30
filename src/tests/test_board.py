import pytest

from src.models.board import Square
from src.models import utils

def test_square_with_invalid_strings(emptyboard):
    invalid_string_squares = ["randomstring",
                              "a0",
                              "a9",
                              "i2"]
    for string in invalid_string_squares:
        with pytest.raises(ValueError):
            Square(string, emptyboard)
        assert emptyboard.square(string) is None

def test_valid_square_attribute_access(emptyboard):
    for column in emptyboard.columns:
        for row in emptyboard.rows:
            square = emptyboard.square(column + row)
            assert square.name == column + row
            assert square.board == emptyboard
            assert square.piece is None

def test_board_place(emptyboard):
    assert not emptyboard.square("a2").piece
    emptyboard.place("white","Pawn","a2")
    assert emptyboard.pieces["white"]["a2"].type == "Pawn"

def test_initial_position(fullboard):
    # There should be 16 pieces of each color
    assert len(fullboard.pieces["white"]) == 16
    assert len(fullboard.pieces["black"]) == 16

    # Checking pieces types and color on all squares matching starting position
    for [color, piece_type, square_label] in utils.starting_position():
        square = fullboard.square(square_label)
        piece = square.piece
        assert piece.type == piece_type
        assert piece.color == color

    #Checking other squares are empty
    occupied = {square for _, _, square in utils.starting_position()}
    for column in fullboard.columns:
        for row in fullboard.rows:
            label = f"{column}{row}"
            if label not in occupied:
                assert fullboard.square(label).piece is None

def test_board_remove(fullboard):
    assert fullboard.square("a2").piece
    fullboard.remove_piece("a2")
    assert not fullboard.square("a2").piece