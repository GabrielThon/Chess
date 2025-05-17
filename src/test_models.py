import pytest

from models import Square, Board, Pawn, Knight, Bishop, Rook, Queen, King
import utils

@pytest.fixture
def emptyboard():
    board = Board(initial_position=False)
    return board

@pytest.fixture
def fullboard():
    board = Board()
    return board

def test_square():
    columns, rows = utils.generate_columns_rows()
    for column in columns:
        for row in rows:
            square = Square(column + row)
            assert square.name == column + row


def test_square_with_invalid_strings():
    invalid_string_squares = ["randomstring",
                              "a0",
                              "a9",
                              "i2"]
    for string in invalid_string_squares:
        with pytest.raises(ValueError):
            Square(string)


def test_square_board_linkage():
    square = Square("a1")
    assert square.board is None

    board = Board(with_squares=False)
    square2 = Square("a1", board)
    assert square2.board == board

def test_board_place(emptyboard):
    assert not emptyboard.square("a2").piece
    emptyboard.place("white","Pawn","a2")
    assert emptyboard.white_pieces[0] == ["Pw","a2"]

def test_board_remove(fullboard):
    assert fullboard.square("a2").piece
    fullboard.remove_piece("a2")
    assert not fullboard.square("a2").piece