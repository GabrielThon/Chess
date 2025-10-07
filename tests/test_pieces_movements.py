import pytest
import json
from pathlib import Path

from chess.models.position import Position

POSITIONS_PATH = Path(__file__).parent / "test_pieces_movements.json"
positions = json.loads(POSITIONS_PATH.read_text())
position_ids = [p["name"] for p in positions]

@pytest.mark.parametrize("scenario", positions, ids=position_ids)
def test_pieces_moving_squares(scenario):
    position = Position([])
    for color, piece_type, square, _ in scenario["position"]:
        position.place_piece(color, piece_type, square)

    for color, piece_type, square_name, expected_moves in scenario["position"]:
        piece = position.square(square_name).piece
        actual_moves = {square.name for square in piece.moving_squares()}
        expected_moves_set = set(expected_moves)

        assert actual_moves == expected_moves_set, f"Failed for {piece_type} {square_name} in position {scenario["name"]}"

