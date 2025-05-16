import pytest

from models import Square
import utils

def test_square():
    columns, rows = utils.generate_columns_rows()
    for column in columns:
        for row in rows:
            square = Square(column+row)
            assert square.name == column+row

def test_square_with_invalid_strings():
    invalid_string_squares = ["randomstring",
                              "a0",
                              "a9",
                              "i2"]
    for string in invalid_string_squares:
        with pytest.raises(ValueError):
            Square(string)
