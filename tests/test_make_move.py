from chess.models.move import Move
from chess.models.position import Position


def test_simple_move():
    position = Position([["white", "King", "e1"],
                         ["black", "King", "e8"]],
                        whose_move="white")
    king_e1 = position.piece("e1")
    square_e2 = position.square("e2")
    move = Move(position, king_e1, square_e2)
    new_position = position.make_move(move)[0]
    assert new_position.square("e1").piece is None
    assert new_position.square("e2").piece is not None
    assert new_position.piece("e2").color == "white"
    assert new_position.piece("e2").type == "King"
    assert new_position.square("e8").piece is not None
    assert new_position.piece("e8").color == "black"
    assert new_position.piece("e8").type == "King"

