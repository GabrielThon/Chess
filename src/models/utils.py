def starting_position():
    return [["white", "Rook", "a1"],
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
    return list("abcdefgh"), [str(i) for i in range(1, 9)]


def is_valid_square_string(string: str) -> bool:
    return (
            len(string) == 2 and
            string[0] in 'abcdefgh' and
            string[1] in '12345678'
    )


def is_valid_color(color: str):
    if color.lower() == "white" or color.lower() == "black":
        return True
    return False


def label_to_indices(label):
    if not is_valid_square_string(label):
        raise ValueError(f"Invalid square label: {label}")
    col = ord(label[0]) - ord('a')
    row = int(label[1]) - 1
    return col, row
