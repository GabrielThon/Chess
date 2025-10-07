import pytest
import json
from pathlib import Path
from chess.models.position import Position

POSITIONS_PATH = Path(__file__).parent / "test_position_checks_and_pins.json"
positions = json.loads(POSITIONS_PATH.read_text())
position_ids = [p["name"] for p in positions]


@pytest.mark.parametrize("scenario", positions, ids=position_ids)
def test_pieces_moving_squares(emptyboard, scenario):
    position = Position(scenario["position"], scenario["move"])
    position.castling_rights["white_kingside"] = False
    position.castling_rights["white_queenside"] = False
    position.compute_legal_moves()

    for color, piece_type, square, expected_moves in scenario["result"]:
        piece = position.piece(square)
        expected_moves_set = set(expected_moves)
        actual_moves_set = {move.end_square.name for move in position.legal_moves_.get(piece,[])}
        assert actual_moves_set == expected_moves_set
