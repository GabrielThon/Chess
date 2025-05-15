import unittest
from models import Board, Square
import utils

class MyTestCase(unittest.TestCase):
    def test_construct_valid_square(self):
        board = Board(with_squares=False)
        columns,rows = board.columns, board.rows
        for col in columns:
            for row in rows:
                new_square = Square(col+row, board)
                self.assertEqual(new_square.name, col+row)

    def test_construct_invalid_squares(self):
        board = Board()
        invalid_string_squares = ["randomstring",
                                  "a0",
                                  "a9",
                                  "i2"]
        for string in invalid_string_squares:
            with self.assertRaises(ValueError) as err:
                Square(string,board)
            self.assertEqual(str(err.exception), f"Wrong argument in the Square constructor : {string}")




if __name__ == '__main__':
    unittest.main()
