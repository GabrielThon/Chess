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


def test_square_isempty():
    square = Square("a1")
    assert square.isempty == True

    piece = Pawn("white")
    piece.place_on_square(square)
    assert square.isempty == False

def test_board_place(emptyboard):
    assert emptyboard["a2"].isempty
    emptyboard.place("white","Pawn","a2")
    assert str(emptyboard.white_pieces[0]) == "Pa2-w"

def test_board_remove(fullboard):
    assert not fullboard["a2"].isempty
    fullboard.remove_piece("a2")
    assert fullboard["a2"].isempty