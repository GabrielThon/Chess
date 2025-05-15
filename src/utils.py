import string
from models import Square, Board
import typing

def generate_columns_rows():
    columns = list(string.ascii_lowercase[:8])
    rows = [str(i) for i in range(1, 9)]
    return columns, rows

def is_valid_string_square(string : str):
    if len(string) != 2:
        return False

    columns = ['a','b','c','d','e','f','g','h']
    if string[0] not in columns :
        return False

    if not string[1].isdigit():
        return False
    row = int(string[1])
    rows = range(1,9,1)
    if row not in rows :
        return False

    return True

def is_valid_color(color : str):
    if color.lower() == "white" or color.lower() == "black":
        return True
    return False

def label_to_indices(label):
    # TO DO : checks on label
    columns = list(string.ascii_lowercase[:8])
    col = columns.index(label[0])
    row = int(label[1]) - 1
    return col, row

def is_at_knight_distance(square1: Square, square2: Square):
    columns, rows = generate_columns_rows()
    column_distance = abs(columns.index(square2.column) - columns.index(square1.column))
    row_distance = abs(rows.index(square2.row) - rows.index(square1.row))
    boolean = column_distance + row_distance == 3 and square1.column != square2.column and square1.row != square2.row
    return boolean

def squares_at_knight_distance(square : Square):
    board = square.board
    return [board[col + row] for col in board.columns for row in board.rows if is_at_knight_distance(board[col + row], square)]

if __name__ == "__main__":
    print(is_valid_string_square("a1"))
    print(is_valid_string_square("h8"))
    print(is_valid_string_square("randomstring"))
    print(is_valid_string_square("a0"))
    print(is_valid_string_square("a9"))
    print(is_valid_string_square("i2"))