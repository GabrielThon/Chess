import pytest
import json
from pathlib import Path
from src.models.position import Position
from src.models import exceptions

POSITIONS_PATH = Path(__file__).parent / "test_checks_and_pins.json"
positions = json.loads(POSITIONS_PATH.read_text())
position_ids = [p["name"] for p in positions]


@pytest.mark.parametrize("scenario", positions, ids=position_ids)
def test_pieces_moving_squares(emptyboard, scenario):
    for color, piece_type, square in scenario["position"]:
        emptyboard.place(color, piece_type, square)

    position = Position(emptyboard, scenario["move"])
    legal_moves = position.legal_moves()

    for color, piece_type, square, expected_moves in scenario["result"]:
        piece = emptyboard.piece(square)
        expected_moves_set = set(expected_moves)
        actual_moves_set = {piece.name for piece in legal_moves[piece]}
        assert actual_moves_set == expected_moves_set
