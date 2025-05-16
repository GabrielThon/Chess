import string
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Square

def starting_position():
    return [["white","Rook","a1"],
            ["white", "Knight", "b1"],
            ["white", "Bishop", "c1"],
            ["white", "Queen", "d1"],
            ["white", "King", "e1"],
            ["white", "Bishop", "f1"],
            ["white", "Knight", "g1"],
            ["white", "Rook", "h1"],
            ["white", "Pawn", "a2"],
            ["white", "Pawn", "b2"],
            ["white", "Pawn", "c2"],
            ["white", "Pawn", "d2"],
            ["white", "Pawn", "e2"],
            ["white", "Pawn", "f2"],
            ["white", "Pawn", "g2"],
            ["white", "Pawn", "h2"],
            ["black", "Rook", "a8"],
            ["black", "Knight", "b8"],
            ["black", "Bishop", "c8"],
            ["black", "Queen", "d8"],
            ["black", "King", "e8"],
            ["black", "Bishop", "f8"],
            ["black", "Knight", "g8"],
            ["black", "Rook", "h8"],
            ["black", "Pawn", "a7"],
            ["black", "Pawn", "b7"],
            ["black", "Pawn", "c7"],
            ["black", "Pawn", "d7"],
            ["black", "Pawn", "e7"],
            ["black", "Pawn", "f7"],
            ["black", "Pawn", "g7"],
            ["black", "Pawn", "h7"],
            ]


def generate_columns_rows():
    columns = list(string.ascii_lowercase[:8])
    rows = [str(i) for i in range(1, 9)]
    return columns, rows


def is_valid_square_string(string: str):
    if len(string) != 2:
        return False

    columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    if string[0] not in columns:
        return False

    if not string[1].isdigit():
        return False
    row = int(string[1])
    rows = range(1, 9, 1)
    if row not in rows:
        return False

    return True


def is_valid_color(color: str):
    if color.lower() == "white" or color.lower() == "black":
        return True
    return False


def label_to_indices(label):
    # TO DO : checks on label
    columns = list(string.ascii_lowercase[:8])
    col = columns.index(label[0])
    row = int(label[1]) - 1
    return col, row


if __name__ == "__main__":
    print(is_valid_square_string("a1"))
    print(is_valid_square_string("h8"))
    print(is_valid_square_string("randomstring"))
    print(is_valid_square_string("a0"))
    print(is_valid_square_string("a9"))
    print(is_valid_square_string("i2"))
